import argparse

from pyguitar.guitar import Fretboard
from pyguitar.notes import MAJOR_SCALE, MINOR_SCALE, note_name_to_int, shift

SCALE_NOTE_COLORS = ["red", "black", "green", "black", "blue", "black", "black"]
SCALE_NOTE_NAMES = ["R", "2", "3", "4", "5", "6", "7"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play with notes")
    parser.add_argument("command", choices=["pentatonic", "triad"])
    parser.add_argument("--minor", action="store_true")
    parser.add_argument("--root", default="C")
    options = parser.parse_args()

    # Determine notes.
    root = note_name_to_int(options.root)
    scale = shift(root, MINOR_SCALE if options.minor else MAJOR_SCALE)
    if options.command == "pentatonic":
        # pentatonic scale
        note_names = ["R", "3", "4", "5", "7"]
    else:
        # major triad
        note_names = ["R", "3", "5"]
    note_indexes = [SCALE_NOTE_NAMES.index(n) for n in note_names]
    note_colors = [SCALE_NOTE_COLORS[i] for i in note_indexes]
    note_values = [scale[i] % 12 for i in note_indexes]

    # Place notes on fretboard.
    board = Fretboard()
    for pos, note_value in board.walk():
        try:
            idx = note_values.index(note_value % 12)
        except ValueError:
            continue
        board.set(pos, {"color": note_colors[idx], "text": note_names[idx]})

    # display fretboard
    print(board.dump())
    with open("board.svg", "w") as fp:
        fp.write(board.dump_svg())
