import argparse

from pychord import Chord
from pychord.utils import note_to_val

from pyguitar.notes import Note

FRETS = 15
STRINGS = [Note.E2, Note.A2, Note.D3, Note.G3, Note.B3, Note.E4]


class Fretboard:
    def __init__(self):
        self._cells = [["" for x in STRINGS] for f in range(FRETS)]

    def dump(self):
        indent = "   "
        width = 31
        lines = []
        for idx, row in enumerate(self._cells):
            row = ["%2s" % x for x in row]
            lines.append(("%.2d | " % idx) + (" | ".join(row)) + " |")
            if idx:
                lines.append(indent + ("-" * width))
            else:
                lines.append(indent + ("=" * width))
        return "\n".join(lines)

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

    note_names = chord.components()
    note_values = [note_to_val(x) for x in note_names]

    print(chord, note_names)
    for pos, note_value in board.walk():
        try:
            idx = note_values.index(note_value % 12)
        except ValueError:
            continue
        board.set(pos, note_names[idx])
    print(board.dump())
