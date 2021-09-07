import argparse

from pychord import Chord
from pychord.utils import note_to_val

from pyguitar.notes import Note

FRETS = 18
STRINGS = [Note.E2, Note.A2, Note.D3, Note.G3, Note.B3, Note.E4]


class Fretboard:
    def __init__(self):
        self._cells = [[None for x in STRINGS] for f in range(FRETS)]

    def dump(self):
        indent = "   "
        width = 31
        lines = []
        for idx, row in enumerate(self._cells):
            row = ["%2s" % (x["text"] if x else "") for x in row]
            lines.append(("%.2d | " % idx) + (" | ".join(row)) + " |")
            if idx:
                lines.append(indent + ("-" * width))
            else:
                lines.append(indent + ("=" * width))
        return "\n".join(lines)

    def dump_svg(self):
        padding = 10
        fret_spacing = 30
        string_spacing = 20
        board_width = string_spacing * (len(STRINGS) - 1)
        board_height = fret_spacing * FRETS
        output = '<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">' % (
            board_width + 2 * padding,
            board_height + 2 * padding,
        )

        # draw strings
        for string_idx, string_note in enumerate(STRINGS):
            x = padding + string_idx * string_spacing
            output += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="black"/>' % (
                x,
                padding,
                x,
                padding + board_height,
            )

        # draw frets
        for fret_idx in range(FRETS + 1):
            y = padding + fret_idx * fret_spacing
            output += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="black"/>' % (
                padding,
                y,
                padding + board_width,
                y,
            )

        # draw markers
        for fret_idx, row in enumerate(self._cells):
            for string_idx, cell in enumerate(row):
                if cell:
                    cx = padding + string_idx * string_spacing
                    cy = padding + (fret_idx + 0.5) * fret_spacing
                    output += (
                        '<circle cx="%d" cy="%d" r="%d" stroke="%s" fill="white" />'
                        % (
                            cx,
                            cy,
                            string_spacing / 2.5,
                            cell["color"],
                        )
                    )
                    output += (
                        '<text x="%d" y="%d" fill="%s" text-anchor="middle">%s</text>'
                        % (cx, cy + 4, cell["color"], cell["text"])
                    )

        output += "</svg>"
        return output

    def set(self, pos, value):
        self._cells[pos[0]][pos[1]] = value

    def walk(self):
        for string_idx, string_note in enumerate(STRINGS):
            for fret in range(FRETS):
                yield (fret, string_idx), string_note + fret


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play with notes")
    parser.add_argument("chord")
    options = parser.parse_args()

    board = Fretboard()
    chord = Chord(options.chord)

    note_colors = ["red", "green", "blue", "black"]
    note_names = chord.components()
    note_values = [note_to_val(x) for x in note_names]

    print(chord, note_names)
    for pos, note_value in board.walk():
        try:
            idx = note_values.index(note_value % 12)
        except ValueError:
            continue
        board.set(pos, {"color": note_colors[idx], "text": note_names[idx]})
    print(board.dump())

    with open("board.svg", "w") as fp:
        fp.write(board.dump_svg())
