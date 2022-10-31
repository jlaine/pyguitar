import argparse

import mido

from pyguitar.chords import (
    chord_name_from_roman,
    chord_name_to_note_names,
    chord_name_to_pitches,
)
from pyguitar.notes import (
    MAJOR_KEYS,
    MAJOR_SCALE_ROMAN,
    MINOR_KEYS,
    MINOR_SCALE_ROMAN,
    key_name_to_note_names,
    prettify_chord,
    prettify_key,
    prettify_note,
)


def print_key_chords(key: str, romans: list[str]) -> None:
    print("== %s key ==" % prettify_key(key))
    for chord_roman in romans:
        chord_name = chord_name_from_roman(chord_roman, key)
        print(
            "%-5s %-4s : %s"
            % (
                chord_roman,
                prettify_chord(chord_name),
                " ".join(
                    [
                        "%-2s" % prettify_note(note)
                        for note in chord_name_to_note_names(chord_name, key)
                    ]
                ),
            )
        )


def parse_strum_pattern(pattern: str, beat_time=480) -> list[list[tuple[str, int]]]:
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
    *, track: mido.MidiTrack, pitches: list[int], strum: list[tuple[str, int]]
):
    for event, time in strum:
        track.append(mido.Message(event, note=pitches[0], time=time))
        for note in pitches[1:]:
            track.append(mido.Message(event, note=note, time=0))


def play_midi_pattern(
    *,
    track: mido.MidiTrack,
    key: str,
    chord_pattern: str,
    strum_pattern: str,
    beats_per_minute=120,
    repeat=1,
):
    track.append(
        mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(beats_per_minute), time=0)
    )
    track.append(mido.Message("program_change", program=26, time=0))

    chord_pattern_roman = chord_pattern.split()
    chord_pattern_name = [chord_name_from_roman(c, key) for c in chord_pattern_roman]

    strum_pattern = parse_strum_pattern(pattern=strum_pattern)
    strum_index = 0
    for _ in range(repeat):
        for chord_name in chord_pattern_name:
            play_midi_chord(
                track=track,
                pitches=tuple(p + 48 for p in chord_name_to_pitches(chord_name)),
                strum=strum_pattern[strum_index],
            )
            strum_index = (strum_index + 1) % len(strum_pattern)

    # print chords
    print_key_chords(key, set(chord_pattern_roman))

    print("== pattern ==")
    print(" ".join(chord_pattern_roman))
    print("== chords ==")
    print(" ".join(chord_pattern_name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play with notes")
    parser.add_argument("command", choices=["chords", "notes", "render"])
    parser.add_argument("--minor", action="store_true")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--song")
    options = parser.parse_args()

    if options.command == "chords":
        for key in MINOR_KEYS if options.minor else MAJOR_KEYS:
            print_key_chords(
                key, MINOR_SCALE_ROMAN if key.islower() else MAJOR_SCALE_ROMAN
            )
    elif options.command == "notes":
        for key in MINOR_KEYS if options.minor else MAJOR_KEYS:
            print(
                "%-8s : %s"
                % (
                    prettify_key(key),
                    " ".join(
                        [
                            "%-2s" % prettify_note(name)
                            for name in key_name_to_note_names(key)
                        ]
                    ),
                )
            )
    else:
        songs = {
            "50s": {
                "chord_pattern": "I vi IV V",
                "key": "C",
            },
            "blueforyou": {
                "beats_per_minute": 90,
                "chord_pattern": "I7 IV7 I7 I7 " + "IV7 IV7 I7 I7 " + "V7 IV7 I7 V7",
                "key": "D",
                "strum_pattern": "D-D-D-D-",
            },
            "blues": {
                "chord_pattern": "I7 I7 I7 I7 IV7 IV7 I7 I7 V7 IV7 I7 V7",
                "key": "A",
            },
            "blues-quick-change": {
                "chord_pattern": "I7 IV7 I7 I7 IV7 IV7 I7 I7 V7 IV7 I7 V7",
                "key": "A",
            },
            "blues-slow-change": {
                "chord_pattern": "I7 I7 I7 I7 IV7 IV7 I7 I7 V7 V7 I7 I7",
                "key": "A",
            },
            "blues7": {
                "beats_per_minute": 130,
                "chord_pattern": "I IV I I7 IV IV7 I I7 V IV I V7",
                "key": "A",
                "strum_pattern": "D-DU-UD-/D-DU-UDU",
            },
            "heyjude": {
                "beats_per_minute": 150,
                "chord_pattern": (
                    "I I V V V7 V7 I I IV IV I I V V7 I I "  # verse
                    + "I7 I7 IV IVmaj7/iii ii7 IV/I V7 V7 I I"  # chorus
                ),
                "key": "F",
                "strum_pattern": "D-D-D-DU",
            },
            "key": {
                "chord_pattern": "I ii iii IV V vi viidim",
                "key": "A",
            },
            "paintitblack": {
                "beats_per_minute": 160,
                "chord_pattern": "i VII III VII i i i i i VII III VII IV IV V/iv V/iv",
                "key": "e",
                "strum_pattern": "D-DU/DUD/U-UD/U-UD-",
            },
            "pop": {
                "key": "C",
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
            key=song["key"],
            chord_pattern=song["chord_pattern"],
            strum_pattern=song.get("strum_pattern", "D-D-D-D-"),
            beats_per_minute=song.get("beats_per_minute", 120),
            repeat=options.repeat,
        )

        mid.save(options.song + ".mid")
