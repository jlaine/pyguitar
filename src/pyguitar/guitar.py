import dataclasses
from typing import Iterator, Optional

from colorama import Back, Fore, Style

from pyguitar.notes import Note

FRETS = 15
STRINGS = [Note.E2, Note.A2, Note.D3, Note.G3, Note.B3, Note.E4]


@dataclasses.dataclass
class Cell:
    color: str
    text: str


class Fretboard:
    def __init__(self) -> None:
        self._cells: list[list[Optional[Cell]]] = [
            [None for x in STRINGS] for f in range(FRETS)
        ]

    def dump(self) -> str:
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
            str_row: list[str] = [
                (
                    (getattr(Fore, cell.color.upper()) + pad(cell.text) + Fore.BLACK)
                    if cell is not None
                    else (Fore.BLACK + pad("|") + Fore.RESET)
                )
                for cell in row
            ]
            lines.append(
                ("%.2d " % idx) + Back.WHITE + "  ".join(str_row) + Style.RESET_ALL
            )
            marker = "-" if idx else "="
            lines.append(
                indent + Back.WHITE + Fore.BLACK + (marker * width) + Style.RESET_ALL
            )
        return "\n".join(lines)

    def dump_svg(self) -> str:
        padding = 10
        fret_spacing = 30
        string_spacing = 20
        board_width = string_spacing * (len(STRINGS) - 1)
        board_height = fret_spacing * FRETS
        output = '<svg viewBox="0 0 %f %f" xmlns="http://www.w3.org/2000/svg">' % (
            board_width + 2 * padding,
            board_height + 2 * padding,
        )

        # draw strings
        for string_idx, string_note in enumerate(STRINGS):
            x = padding + string_idx * string_spacing
            output += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="black"/>' % (
                x,
                padding,
                x,
                padding + board_height,
            )

        # draw frets
        for fret_idx in range(FRETS + 1):
            y = padding + fret_idx * fret_spacing
            output += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="black"/>' % (
                padding,
                y,
                padding + board_width,
                y,
            )

        # draw markers
        for fret_idx, row in enumerate(self._cells):
            for string_idx, cell in enumerate(row):
                if cell is not None:
                    cx = padding + string_idx * string_spacing
                    cy = padding + (fret_idx + 0.5) * fret_spacing
                    output += (
                        '<circle cx="%d" cy="%f" r="%f" stroke="%s" fill="white" />'
                        % (
                            cx,
                            cy,
                            string_spacing / 2.5,
                            cell.color,
                        )
                    )
                    output += (
                        '<text x="%f" y="%f" fill="%s" font-family="arial" font-size="12px" text-anchor="middle">%s</text>'
                        % (cx, cy + 4, cell.color, cell.text)
                    )

        output += "</svg>"
        return output

    def set(self, pos: tuple[int, int], value: Optional[Cell]) -> None:
        self._cells[pos[0]][pos[1]] = value

    def walk(self) -> Iterator[tuple[tuple[int, int], int]]:
        for string_idx, string_note in enumerate(STRINGS):
            for fret in range(FRETS):
                yield (fret, string_idx), string_note + fret
