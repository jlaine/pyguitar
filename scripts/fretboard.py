import argparse

from pychord import Chord
from pychord.utils import note_to_val
from pyguitar.guitar import Fretboard
from pyguitar.notes import Namer, shift


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play with notes")
    parser.add_argument("command", choices=["chord", "pentatonic"])
    parser.add_argument("--chord", default="C")
    options = parser.parse_args()

    board = Fretboard()

    if options.command == "pentatonic":
        # minor pentatonic
        root = note_to_val(options.chord)
        namer = Namer(root)
        note_colors = ["red", "green", "black", "blue", "black"]
        note_values = [x % 12 for x in shift(root, (0, 3, 5, 7, 10))]
        note_names = [namer.name_note(x) for x in note_values]
        note_names = ["R", "3", "4", "5", "7"]
    else:
        # major chord
        chord = Chord(options.chord)
        note_colors = ["red", "green", "blue", "black"]
        note_names = chord.components()
        note_values = [note_to_val(x) for x in note_names]
        note_names = ["R", "3", "5"]

    # place notes on fretboard
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
