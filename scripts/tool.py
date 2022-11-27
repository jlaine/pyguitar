import argparse
import dataclasses
from fractions import Fraction
from typing import Iterable

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
from pyguitar.tracks import Track


@dataclasses.dataclass
class Song:
    chord_pattern: str
    key: str
    beats_per_minute: int = 120
    strum_pattern: str = "D-D-D-D-"


def print_key_chords(key: str, romans: Iterable[str]) -> None:
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


def print_song_info(song: Song):
    chord_pattern_roman = song.chord_pattern.split()
    chord_pattern_name = [
        chord_name_from_roman(c, song.key) for c in chord_pattern_roman
    ]

    # Print chord pattern.
    print_key_chords(song.key, set(chord_pattern_roman))
    print("== chord pattern ==")
    print(" ".join("%-3s" % x for x in chord_pattern_roman))
    print(" ".join("%-3s" % x for x in chord_pattern_name))

    # Print strumming pattern.
    print("== strumming pattern ==")
    print(song.strum_pattern)


def strum_song(*, repeat: int, song: Song):
    track = Track(beats_per_minute=song.beats_per_minute)

    chord_pattern_roman = song.chord_pattern.split()
    chord_pattern_name = [
        chord_name_from_roman(c, song.key) for c in chord_pattern_roman
    ]

    half_beat = Fraction(1, 2)
    strum_events: list[list[Fraction]] = []
    for chunk in song.strum_pattern.split("/"):
        events = []
        assert chunk[0] in ("D", "U"), "strum pattern chunk must start with a strum"
        for strum in chunk:
            if strum in ("D", "U"):
                events.append(half_beat)
            else:
                assert strum == "-"
                events[-1] += half_beat
        strum_events.append(events)

    strum_index = 0
    for _ in range(repeat):
        for chord_name in chord_pattern_name:
            pitches = [p + 48 for p in chord_name_to_pitches(chord_name)]
            for duration in strum_events[strum_index]:
                track.add_notes(duration=duration, pitches=pitches)
            strum_index = (strum_index + 1) % len(strum_events)

    return track


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
            "50s": Song(
                chord_pattern="I vi IV V",
                key="C",
            ),
            "50-ways-to-leave-your-lover": Song(
                chord_pattern="i/III VII6 VImaj7 V7b9 "
                + "i VII#dim7 IIdim7 Vaug7 "
                + "i VII6 VImaj7 V7b9 "
                + "i iv7 i",
                key="e",
                strum_pattern="D---",
            ),
            "blueforyou": Song(
                beats_per_minute=90,
                chord_pattern="I7 IV7 I7 I7 " + "IV7 IV7 I7 I7 " + "V7 IV7 I7 V7",
                key="D",
            ),
            "blues": Song(
                chord_pattern="I7 I7 I7 I7 IV7 IV7 I7 I7 V7 IV7 I7 V7",
                key="a",
            ),
            "blues-quick-change": Song(
                chord_pattern="I7 IV7 I7 I7 IV7 IV7 I7 I7 V7 IV7 I7 V7",
                key="a",
            ),
            "blues-slow-change": Song(
                chord_pattern="I7 I7 I7 I7 IV7 IV7 I7 I7 V7 V7 I7 I7",
                key="a",
            ),
            "blues7": Song(
                chord_pattern="I IV I I7 IV IV7 I I7 V IV I V7",
                key="a",
                strum_pattern="D-DU-UD-/D-DU-UDU",
            ),
            "heyjude": Song(
                beats_per_minute=150,
                chord_pattern=(
                    "I I V V V7 V7 I I IV IV I I V V7 I I "  # verse
                    + "I7 I7 IV IVmaj7/iii ii7 IV/I V7 V7 I I"  # chorus
                ),
                key="F",
                strum_pattern="D-D-D-DU",
            ),
            "key": Song(
                chord_pattern="I ii iii IV V vi viidim",
                key="A",
            ),
            "paintitblack": Song(
                beats_per_minute=160,
                chord_pattern="i VII III VII i i i i i VII III VII IV IV V/iv V/iv",
                key="e",
                strum_pattern="D-DU/DUD/U-UD/U-UD-",
            ),
            "pop": Song(
                chord_pattern="I V vi IV",
                key="C",
            ),
        }
        assert options.song in songs, "Please specify a song with --song"
        song = songs[options.song]

        print_song_info(song)
        track = strum_song(repeat=options.repeat, song=song)

        # Save to MIDI file.
        mid_file = mido.MidiFile()
        mid_file.tracks.append(track.to_midi())
        mid_file.save(options.song + ".mid")
