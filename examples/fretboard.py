import argparse
import sys

from pyfrets.chords import (
    chord_name_to_interval_names,
    chord_name_to_note_names,
    chord_name_to_pitches,
)
from pyfrets.guitar import Cell, Fretboard, Orientation
from pyfrets.notes import (
    key_name_to_note_names,
    key_name_to_pitches,
    prettify_interval,
    prettify_note,
)

SCALE_NOTE_COLORS = ["red", "black", "green", "magenta", "blue", "black", "magenta"]
DIATONIC_NOTE_FUNCTIONS = ["R", "2", "3", "4", "5", "6", "7"]
PENTATONIC_NOTE_FUNCTIONS = ["R", "3", "4", "5", "7"]


def plot_notes(
    *,
    basename: str,
    note_colors: list[str],
    note_texts: list[str],
    note_values: list[int],
    orientation: Orientation,
) -> None:
    # Place notes on fretboard.
    board = Fretboard()
    note_values = [i % 12 for i in note_values]
    for pos, note_value in board.walk():
        try:
            idx = note_values.index(note_value % 12)
        except ValueError:
            continue
        board.set(pos, Cell(color=note_colors[idx], text=note_texts[idx]))

    # Display fretboard.
    sys.stdout.write(board.dump_ansi(orientation=orientation))

    # Write files.
    with open(basename + ".svg", "w") as fp:
        fp.write(board.dump_svg(orientation=orientation))


def main() -> None:
    parser = argparse.ArgumentParser(description="Display notes on a guitar")
    parser.add_argument(
        "--note-names",
        action="store_true",
        help="Show note names instead of their function.",
    )
    parser.add_argument(
        "--portrait",
        action="store_true",
        help="Show the fretboard in portrait mode.",
    )

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="The command to run."
    )
    subparser = subparsers.add_parser("scale", help="Show the notes of a scale.")
    subparser.add_argument("--pentatonic", action="store_true")
    subparser.add_argument("key")

    subparser = subparsers.add_parser("chord", help="Show the notes of a chord.")
    subparser.add_argument("chord")
    options = parser.parse_args()

    if options.portrait:
        orientation = Orientation.PORTRAIT
    else:
        orientation = Orientation.LANDSCAPE

    # Determine notes.
    if options.command == "scale":
        names = key_name_to_note_names(options.key)
        pitches = key_name_to_pitches(options.key)
        if options.pentatonic:
            # Pentatonic scale.
            note_functions = PENTATONIC_NOTE_FUNCTIONS
            scale_type = "pentatonic"
        else:
            # Diatonic scale.
            note_functions = DIATONIC_NOTE_FUNCTIONS
            scale_type = "diatonic"

        if options.key[0] == options.key[0].upper():
            key_type = "major"
        else:
            key_type = "minor"
        note_indexes = [DIATONIC_NOTE_FUNCTIONS.index(n) for n in note_functions]
        note_names = [prettify_interval(names[i]) for i in note_indexes]
        note_values = [pitches[i] for i in note_indexes]

        # Display note names.
        for function, name in zip(note_functions, note_names):
            sys.stdout.write(f"{function} = {name}\n")

        plot_notes(
            basename=f"{scale_type}-{options.key.lower()}-{key_type}",
            note_colors=[SCALE_NOTE_COLORS[i] for i in note_indexes],
            note_texts=note_names if options.note_names else note_functions,
            note_values=note_values,
            orientation=orientation,
        )

    else:
        note_functions = [
            prettify_interval(i) for i in chord_name_to_interval_names(options.chord)
        ]
        note_names = [prettify_note(n) for n in chord_name_to_note_names(options.chord)]
        note_values = chord_name_to_pitches(options.chord)

        # Display note names.
        for function, name in zip(note_functions, note_names):
            sys.stdout.write(f"{function:3} = {name}\n")

        plot_notes(
            basename=f"chord-{options.chord}",
            note_colors=[SCALE_NOTE_COLORS[i] for i in range(len(note_values))],
            note_texts=note_names if options.note_names else note_functions,
            note_values=note_values,
            orientation=orientation,
        )


if __name__ == "__main__":
    main()
