import argparse
from typing import Dict, List, Tuple

import mido

from pyguitar.notes import (
    MAJOR_SCALE,
    MAJOR_TRIAD,
    MINOR_SCALE,
    Namer,
    Note,
    scale_chords,
    shift,
)


def print_scale_chords(root: int, minor: bool, chords: Dict[str, List[int]]) -> None:
    namer = Namer(root)

    print("==", namer.name_note(root), "minor" if minor else "major", "key", "==")
    for num, chord in chords.items():
        print(
            "%-5s %-4s : %s"
            % (
                num,
                namer.name_chord(chord),
                " ".join(["%-2s" % namer.name_note(note) for note in chord]),
            )
        )


def print_scale_notes(root: int, minor: bool) -> None:
    namer = Namer(root)
    if minor:
        pitches = MINOR_SCALE
    else:
        pitches = MAJOR_SCALE
    scale = shift(root, pitches)
    print(
        "%-8s : %s"
        % (
            namer.name_scale(scale),
            " ".join(["%-2s" % namer.name_note(note) for note in scale]),
        )
    )


def parse_chord_pattern(root: int, minor: bool, pattern: str) -> List[List[int]]:
    chords = scale_chords(root, minor)
    for bit in ["IV", "V"]:
        if bit not in chords:
            chords[bit] = shift(chords[bit.lower()][0], MAJOR_TRIAD)

    output = []
    for bit in pattern.split():
        if "/" in bit:
            base_roman, over_roman = bit.split("/")
        else:
            base_roman, over_roman = bit, None
        chord = list(chords[base_roman])
        if over_roman is not None:
            over_note = chords[over_roman][0]
            chord.insert(0, over_note)
        output.append(chord)
    return output


def parse_strum_pattern(pattern: str, beat_time=480) -> List[List[Tuple[str, int]]]:
    output = []
    for chunk in pattern.split("/"):
        events = []
        assert chunk[0] in ("D", "U"), "strum pattern chunk must start with a strum"
        for strum in chunk:
            if strum in ("D", "U"):
                events += [
                    ("note_on", 0),
                    ("note_off", int(beat_time / 2)),
                ]
            else:
                assert strum == "-"
                events[-1] = (events[-1][0], events[-1][1] + int(beat_time / 2))
        output.append(events)
    return output


def play_midi_chord(
    *, track: mido.MidiTrack, chord: List[int], strum: List[Tuple[str, int]]
):
    for event, time in strum:
        track.append(mido.Message(event, note=chord[0], time=time))
        for note in chord[1:]:
            track.append(mido.Message(event, note=note, time=0))


def play_midi_pattern(
    *,
    track: mido.MidiTrack,
    root: int,
    minor: bool,
    chord_pattern: str,
    strum_pattern: str,
    beats_per_minute=120,
    repeat=1,
):
    track.append(
        mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(beats_per_minute), time=0)
    )
    track.append(mido.Message("program_change", program=26, time=0))

    pattern_chords = parse_chord_pattern(root=root, minor=minor, pattern=chord_pattern)
    strum_pattern = parse_strum_pattern(pattern=strum_pattern)
    strum_index = 0
    for _ in range(repeat):
        for chord in pattern_chords:
            play_midi_chord(
                track=track,
                chord=chord,
                strum=strum_pattern[strum_index],
            )
            strum_index = (strum_index + 1) % len(strum_pattern)

    namer = Namer(root)

    # print key
    used = set(tuple(x) for x in pattern_chords)
    key_chords = dict(
        x for x in scale_chords(root, minor).items() if tuple(x[1]) in used
    )
    print_scale_chords(root, minor, key_chords)

    print("== pattern ==")
    print(chord_pattern)
    print("== chords ==")
    print(" ".join(namer.name_chord(x) for x in pattern_chords))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play with notes")
    parser.add_argument("command", choices=["chords", "notes", "render"])
    parser.add_argument("--minor", action="store_true")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--song")
    options = parser.parse_args()

    if options.command == "chords":
        for root in [
            Note.C3,
            Note.G3,
            Note.D3,
            Note.A3,
            Note.E3,
            Note.B3,
            Note.G3 - 1,
            Note.D3 - 1,
            Note.A3 - 1,
            Note.E3 - 1,
            Note.B3 - 1,
            Note.F3,
        ]:
            chords = scale_chords(root, minor=options.minor, sevenths=False)
            print_scale_chords(root, minor=options.minor, chords=chords)
    elif options.command == "notes":
        for root in range(Note.C3, Note.C4):
            print_scale_notes(root, minor=options.minor)
    else:
        songs = {
            "50s": {
                "chord_pattern": "I vi IV V",
            },
            "blues": {
                "chord_pattern": "I I I I IV IV I I V IV I V",
            },
            "blues7": {
                "beats_per_minute": 130,
                "chord_pattern": "I IV I I7 IV IV7 I I7 V IV I V7",
                "strum_pattern": "D-DU-UD-/D-DU-UDU",
            },
            "heyjude": {
                "beats_per_minute": 150,
                "chord_pattern": (
                    "I I V V V7 V7 I I IV IV I I V V7 I I "  # verse
                    + "I7 I7 IV IVmaj7/iii ii7 IV/I V7 V7 I I"  # chorus
                ),
                "root": Note.F3,
                "strum_pattern": "D-D-D-DU",
            },
            "key": {
                "chord_pattern": "I ii iii IV V vi vii°",
            },
            "paintitblack": {
                "beats_per_minute": 160,
                "chord_pattern": "i VII III VII i i i i i VII III VII IV IV V/iv V/iv",
                "root": Note.E3,
                "strum_pattern": "D-DU/DUD/U-UD/U-UD-",
            },
            "pop": {
                "pattern": "I V vi IV",
            },
        }
        assert options.song in songs, "Please specify a song with --song"
        song = songs[options.song]

        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)

        play_midi_pattern(
            track=track,
            root=song.get("root", Note.C3),
            minor=song["chord_pattern"].startswith("i"),
            chord_pattern=song["chord_pattern"],
            strum_pattern=song.get("strum_pattern", "D-D-D-D-"),
            beats_per_minute=song.get("beats_per_minute", 120),
            repeat=options.repeat,
        )

        mid.save(options.song + ".mid")
