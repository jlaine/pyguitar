import argparse

from pychord import Chord
from pychord.utils import note_to_val

from pyguitar.notes import MINOR_SCALE, Namer, Note, shift

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
                if cell:
                    cx = padding + string_idx * string_spacing
                    cy = padding + (fret_idx + 0.5) * fret_spacing
                    output += (
                        '<circle cx="%d" cy="%f" r="%f" stroke="%s" fill="white" />'
                        % (
                            cx,
                            cy,
                            string_spacing / 2.5,
                            cell["color"],
                        )
                    )
                    output += (
                        '<text x="%f" y="%f" fill="%s" font-family="arial" font-size="12px" text-anchor="middle">%s</text>'
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

    if True:
        # major chord
        chord = Chord(options.chord)
        note_colors = ["red", "green", "blue", "black"]
        note_names = chord.components()
        note_values = [note_to_val(x) for x in note_names]
        note_names = ["R", "3", "5"]
    else:
        # minor pentatonic
        root = note_to_val(options.chord)
        namer = Namer(root)
        note_colors = ["red", "green", "black", "blue", "black"]
        note_values = [x % 12 for x in shift(root, (0, 3, 5, 7, 10))]
        note_names = [namer.name_note(x) for x in note_values]
        note_names = ["R", "3", "4", "5", "7"]

    for pos, note_value in board.walk():
        try:
            idx = note_values.index(note_value % 12)
        except ValueError:
            continue
        board.set(pos, {"color": note_colors[idx], "text": note_names[idx]})
    print(board.dump())

    with open("board.svg", "w") as fp:
        fp.write(board.dump_svg())
