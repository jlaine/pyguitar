import dataclasses
import enum
import io
from typing import Iterator, Optional

import pydyf
from colorama import Back, Fore, Style

from pyguitar.notes import Note

FRETS = 16
STRINGS = [Note.E2, Note.A2, Note.D3, Note.G3, Note.B3, Note.E4]

PDF_COLORS = {
    "black": (0, 0, 0),
    "blue": (0, 0, 1),
    "green": (0, 0.5, 0),
    "magenta": (1, 0, 1),
    "red": (1, 0, 0),
    "white": (1, 1, 1),
}


@dataclasses.dataclass
class Cell:
    color: str
    text: str


class Orientation(enum.Enum):
    PORTRAIT = "PORTRAIT"
    LANDSCAPE = "LANDSCAPE"


class PdfPainter:
    def __init__(self, draw: pydyf.Stream, rotate_text: bool) -> None:
        self.draw = draw
        self.rotate_text = rotate_text

    def draw_circle(
        self, *, cx: float, cy: float, radius: float, fill: str, stroke: str
    ) -> None:
        """
        Draw an approximate circle using 4 bezier curves.
        """
        c = 0.55228474983079
        self.draw.push_state()
        self.draw.set_matrix(1, 0, 0, 1, cx, -cy)
        self.draw.move_to(self._x(0), self._y(radius))
        self.draw.curve_to(
            self._x(c * radius),
            self._y(radius),
            self._x(radius),
            self._y(c * radius),
            self._x(radius),
            self._y(0),
        )
        self.draw.curve_to(
            self._x(radius),
            self._y(-c * radius),
            self._x(c * radius),
            self._y(-radius),
            self._x(0),
            self._y(-radius),
        )
        self.draw.curve_to(
            self._x(-c * radius),
            self._y(-radius),
            self._x(-radius),
            self._y(-c * radius),
            self._x(-radius),
            self._y(0),
        )
        self.draw.curve_to(
            self._x(-radius),
            self._y(c * radius),
            self._x(-c * radius),
            self._y(radius),
            self._x(0),
            self._y(radius),
        )
        self.draw.set_color_rgb(*PDF_COLORS[stroke], stroke=True)
        self.draw.set_color_rgb(*PDF_COLORS[fill], stroke=False)
        self.draw.fill_and_stroke()
        self.draw.pop_state()

    def draw_line(
        self,
        *,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        stroke: str,
        stroke_width: float,
    ) -> None:
        self.draw.push_state()
        self.draw.set_color_rgb(*PDF_COLORS[stroke], stroke=True)
        self.draw.set_line_width(stroke_width)
        self.draw.move_to(self._x(x1), self._y(y1))
        self.draw.line_to(self._x(x2), self._y(y2))
        self.draw.stroke()
        self.draw.pop_state()

    def draw_text(self, *, cx: float, cy: float, text: str, fill: str) -> None:
        font_size = 12
        letter_width = 4

        self.draw.push_state()
        self.draw.set_color_rgb(*PDF_COLORS[fill], stroke=False)
        self.draw.begin_text()
        if self.rotate_text:
            self.draw.set_matrix(0, -1, 1, 0, 0, 0)
            self.draw.move_text_to(
                self._x(cy - len(text) * letter_width), self._y(4 - cx)
            )
        else:
            self.draw.move_text_to(
                self._x(cx - len(text) * letter_width), self._y(cy + 4)
            )
        self.draw.set_font_size("F1", font_size)
        self.draw.show_text(pydyf.String(text.encode("macroman")))
        self.draw.end_text()
        self.draw.pop_state()

    def _x(self, x: float) -> float:
        return x

    def _y(self, y: float) -> float:
        """
        Keep the Y axis pointing down, like SVG.
        """
        return -y


class SvgPainter:
    def __init__(self, rotate_text: bool) -> None:
        self.output = ""
        self.text_angle = 90 if rotate_text else 0

    def draw_circle(
        self, *, cx: float, cy: float, radius: float, fill: str, stroke: str
    ) -> None:
        self.output += (
            f'<circle cx="{cx}" cy="{cy}" r="{radius}"'
            f' fill="{fill}" stroke="{stroke}"/>'
        )

    def draw_line(
        self,
        *,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        stroke: str,
        stroke_width: float,
    ) -> None:
        self.output += (
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"'
            f' stroke="{stroke}" stroke-width="{stroke_width}"/>'
        )

    def draw_text(self, *, cx: float, cy: float, text: str, fill: str) -> None:
        font_family = "arial"
        font_size = "12"

        self.output += (
            f'<text x="{cx}" y="{cy + 4}" fill="{fill}"'
            f' font-family="{font_family}" font-size="{font_size}px"'
            f' text-anchor="middle"'
            f' transform="rotate({self.text_angle}, {cx}, {cy})">'
            f"{text}</text>"
        )


class Fretboard:
    def __init__(self) -> None:
        self._cells: list[list[Optional[Cell]]] = [
            [None for x in STRINGS] for f in range(FRETS)
        ]
        self._padding = 10
        self._fret_spacing = 30
        self._string_spacing = 20
        self._board_width = self._string_spacing * (len(STRINGS) - 1)
        self._board_height = self._fret_spacing * FRETS
        self._image_width = self._board_width + 4 * self._padding
        self._image_height = self._board_height + 2 * self._padding

    def dump_ansi(self, *, orientation: Orientation) -> str:
        if orientation == Orientation.LANDSCAPE:
            return self.dump_ansi_landscape()
        else:
            return self.dump_ansi_portrait()

    def dump_ansi_landscape(self) -> str:
        def pad(i: str) -> str:
            if len(i) == 1:
                return "-" + i + "-"
            elif len(i) == 2:
                return "-" + i
            else:
                return i

        lines = []
        empty_line = "   ||" + ("   |" * (FRETS - 1))
        for string_idx in range(len(STRINGS) - 1, -1, -1):
            cells = [row[string_idx] for row in self._cells]
            line = "".join(
                (
                    getattr(Fore, cell.color.upper()) + pad(cell.text) + Fore.BLACK
                    if cell is not None
                    else (Fore.BLACK + pad("-") + Fore.RESET)
                )
                + Fore.BLACK
                + ("|" if idx else "||")
                for idx, cell in enumerate(cells)
            )
            lines.append(Back.WHITE + line)
            if string_idx:
                lines.append(Back.WHITE + Fore.BLACK + empty_line)
            else:
                lines.append(
                    Fore.WHITE
                    + "".join([f"{i:02}  " + ("" if i else " ") for i in range(FRETS)])
                )
        return "".join(line + Style.RESET_ALL + "\n" for line in lines)

    def dump_ansi_portrait(self) -> str:
        def pad(i: str) -> str:
            if len(i) == 1:
                return " " + i + " "
            elif len(i) == 2:
                return " " + i
            else:
                return i

        indent = "   "
        lines = []
        width = 5 * len(STRINGS) - 2
        for idx, row in enumerate(self._cells):
            line = "  ".join(
                (
                    (getattr(Fore, cell.color.upper()) + pad(cell.text) + Fore.BLACK)
                    if cell is not None
                    else (Fore.BLACK + pad("|") + Fore.RESET)
                )
                for cell in row
            )
            lines.append(f"{idx:02} " + Back.WHITE + line)
            marker = "-" if idx else "="
            lines.append(indent + Back.WHITE + Fore.BLACK + (marker * width))
        return "".join(line + Style.RESET_ALL + "\n" for line in lines)

    def dump_pdf(self, *, orientation: Orientation) -> bytes:
        if orientation == Orientation.LANDSCAPE:
            doc_matrix = [0, 1, -1, 0, 0, 2 * self._padding]
            doc_viewbox = [0, 0, self._image_height, self._image_width]
        else:
            doc_matrix = [1, 0, 0, 1, 2 * self._padding, self._image_height]
            doc_viewbox = [0, 0, self._image_width, self._image_height]

        draw = pydyf.Stream()
        draw.set_matrix(*doc_matrix)

        painter = PdfPainter(
            draw=draw, rotate_text=orientation == Orientation.LANDSCAPE
        )
        self._draw(painter)

        # Assemble PDF.
        font = pydyf.Dictionary(
            {
                "Type": "/Font",
                "Subtype": "/Type1",
                "Name": "/F1",
                "BaseFont": "/Roboto Regular",
                "Encoding": "/MacRomanEncoding",
            }
        )
        document = pydyf.PDF()
        document.add_object(font)
        document.add_object(draw)
        document.add_page(
            pydyf.Dictionary(
                {
                    "Type": "/Page",
                    "Parent": document.pages.reference,
                    "Contents": draw.reference,
                    "MediaBox": pydyf.Array(doc_viewbox),
                    "Resources": pydyf.Dictionary(
                        {
                            "ProcSet": pydyf.Array(["/PDF", "/Text"]),
                            "Font": pydyf.Dictionary({"F1": font.reference}),
                        }
                    ),
                }
            )
        )

        buf = io.BytesIO()
        document.write(buf)
        return buf.getvalue()

    def dump_svg(self, *, orientation: Orientation) -> str:
        if orientation == Orientation.LANDSCAPE:
            svg_transform = (
                f"translate(0, {self._image_width - 2 * self._padding}) "
                "rotate(-90, 0, 0)"
            )
            svg_viewbox = f"0 0 {self._image_height} {self._image_width}"
        else:
            svg_transform = f"translate({2 * self._padding}, 0)"
            svg_viewbox = f"0 0 {self._image_width} {self._image_height}"

        painter = SvgPainter(rotate_text=orientation == Orientation.LANDSCAPE)
        self._draw(painter)

        output = f'<svg viewBox="{svg_viewbox}" xmlns="http://www.w3.org/2000/svg">'
        output += f'<g transform="{svg_transform}">'
        output += painter.output
        output += "</g></svg>"
        return output

    def set(self, pos: tuple[int, int], value: Optional[Cell]) -> None:
        self._cells[pos[0]][pos[1]] = value

    def walk(self) -> Iterator[tuple[tuple[int, int], int]]:
        for string_idx, string_note in enumerate(STRINGS):
            for fret in range(FRETS):
                yield (fret, string_idx), string_note + fret

    def _draw(self, painter: PdfPainter | SvgPainter) -> None:
        # Draw strings
        for string_idx, string_note in enumerate(STRINGS):
            x = self._padding + string_idx * self._string_spacing
            painter.draw_line(
                x1=x,
                y1=self._padding,
                x2=x,
                y2=self._padding + self._board_height,
                stroke="black",
                stroke_width=1,
            )

        # Draw frets.
        for fret_idx in range(FRETS + 1):
            y = self._padding + fret_idx * self._fret_spacing
            painter.draw_line(
                x1=self._padding,
                y1=y,
                x2=self._padding + self._board_width,
                y2=y,
                stroke="black",
                stroke_width=2 if fret_idx == 1 else 1,
            )

        # Draw markers and number frets.
        for fret_idx, row in enumerate(self._cells):
            cx = -self._padding
            cy = self._padding + (fret_idx + 0.5) * self._fret_spacing

            painter.draw_text(
                cx=cx,
                cy=cy,
                text=str(fret_idx),
                fill="black",
            )

            for string_idx, cell in enumerate(row):
                if cell is not None:
                    cx = self._padding + string_idx * self._string_spacing
                    painter.draw_circle(
                        cx=cx,
                        cy=cy,
                        radius=self._string_spacing / 2.5,
                        fill="white",
                        stroke=cell.color,
                    )
                    painter.draw_text(
                        cx=cx,
                        cy=cy,
                        text=cell.text,
                        fill=cell.color,
                    )
