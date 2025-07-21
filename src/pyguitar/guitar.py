import dataclasses
import enum
from typing import Iterator, Optional

from colorama import Back, Fore, Style

from pyguitar.notes import Note

FRETS = 16
FRET_MARKERS = [0, 3, 5, 7, 9]
STRINGS = [Note.E2, Note.A2, Note.D3, Note.G3, Note.B3, Note.E4]


@dataclasses.dataclass
class Cell:
    color: str
    text: str


class Orientation(enum.Enum):
    PORTRAIT = "PORTRAIT"
    LANDSCAPE = "LANDSCAPE"


class Fretboard:
    def __init__(self) -> None:
        self._cells: list[list[Optional[Cell]]] = [
            [None for x in STRINGS] for f in range(FRETS)
        ]

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
                    + "".join(
                        [
                            (Style.BRIGHT if (i % 12) in FRET_MARKERS else Style.NORMAL)
                            + f"{i:02}  "
                            + ("" if i else " ")
                            for i in range(FRETS)
                        ]
                    )
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

    def dump_svg(self, *, orientation: Orientation) -> str:
        font_family = "arial"
        font_size = "12px"
        padding = 10
        fret_spacing = 30
        string_spacing = 20
        board_width = string_spacing * (len(STRINGS) - 1)
        board_height = fret_spacing * FRETS
        image_width = board_width + 4 * padding
        image_height = board_height + 2 * padding

        if orientation == Orientation.LANDSCAPE:
            svg_transform = (
                f"translate(0, {image_width - 2 * padding}) rotate(-90, 0, 0)"
            )
            svg_viewbox = f"0 0 {image_height} {image_width}"
            text_angle = 90
        else:
            svg_transform = f"translate({2 * padding}, 0)"
            svg_viewbox = f"0 0 {image_width} {image_height}"
            text_angle = 0

        output = f'<svg viewBox="{svg_viewbox}" xmlns="http://www.w3.org/2000/svg">'
        output += f'<g transform="{svg_transform}">'

        # Draw strings
        for string_idx, string_note in enumerate(STRINGS):
            x = padding + string_idx * string_spacing
            output += (
                f'<line x1="{x}" y1="{padding}"'
                f' x2="{x}" y2="{padding + board_height}" stroke="black"/>'
            )

        # Draw frets.
        for fret_idx in range(FRETS + 1):
            y = padding + fret_idx * fret_spacing
            output += (
                f'<line x1="{padding}" y1="{y}"'
                f' x2="{padding + board_width}" y2="{y}"'
                f' stroke="black" stroke-width="{2 if fret_idx == 1 else 1}"/>'
            )

        # Draw markers and number frets.
        for fret_idx, row in enumerate(self._cells):
            cx = -padding
            cy = padding + (fret_idx + 0.5) * fret_spacing

            font_weight = "bold" if (fret_idx % 12) in FRET_MARKERS else "normal"
            output += (
                f'<text x="{cx}" y="{cy + 4}"'
                f' font-family="{font_family}" font-size="{font_size}"'
                f' font-weight="{font_weight}" text-anchor="middle"'
                f' transform="rotate({text_angle}, {cx}, {cy})">'
                f"{fret_idx}</text>\n"
            )

            for string_idx, cell in enumerate(row):
                if cell is not None:
                    cx = padding + string_idx * string_spacing
                    output += (
                        f'<circle cx="{cx}" cy="{cy}" r="{string_spacing / 2.5}"'
                        f' stroke="{cell.color}" fill="white" />'
                    )
                    output += (
                        f'<text x="{cx}" y="{cy + 4}" fill="{cell.color}"'
                        f' font-family="{font_family}" font-size="{font_size}"'
                        ' text-anchor="middle"'
                        f' transform="rotate({text_angle}, {cx}, {cy})">'
                        f"{cell.text}</text>"
                    )

        output += "</g></svg>"
        return output

    def set(self, pos: tuple[int, int], value: Optional[Cell]) -> None:
        self._cells[pos[0]][pos[1]] = value

    def walk(self) -> Iterator[tuple[tuple[int, int], int]]:
        for string_idx, string_note in enumerate(STRINGS):
            for fret in range(FRETS):
                yield (fret, string_idx), string_note + fret
