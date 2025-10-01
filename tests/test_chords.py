import unittest

from pyguitar.chords import (
    chord_name_from_pitches,
    chord_name_from_roman,
    chord_name_to_note_names,
    chord_name_to_pitches,
)


class ChordsTest(unittest.TestCase):
    def test_chord_name_from_roman(self) -> None:
        chords = {
            # major
            "I": "C",
            "II": "D",
            "III": "E",
            "IV": "F",
            "V": "G",
            "VI": "A",
            "VII": "B",
            # minor
            "i": "Cm",
            "ii": "Dm",
            "ii7": "Dm7",
            "iii": "Em",
            "iv": "Fm",
            "v": "Gm",
            "vi": "Am",
            "vii": "Bm",
            # other
            "VIIdim": "Bdim",
            "I7": "C7",
            "IVmaj7": "Fmaj7",
            "IV/I": "F/C",
        }
        key = "C"
        for roman, name in chords.items():
            with self.subTest(roman=roman, key=key):
                self.assertEqual(chord_name_from_roman(roman, key), name)

        with self.assertRaises(ValueError):
            chord_name_from_roman("VV", key)

    def test_chord_name_from_roman_minor_key(self) -> None:
        chords = {
            "I": "E",
            "II": "F#",
            "III": "G",
            "IV": "A",
            "V": "B",
            "VI": "C",
            "VII": "D",
            "VII#": "D#",
            "VIIdim": "Ddim",
            "viidim": "Ddim",
        }
        key = "e"
        for roman, name in chords.items():
            with self.subTest(roman=roman, key=key):
                self.assertEqual(chord_name_from_roman(roman, key), name)

    def test_chord_name_to_note_names(self) -> None:
        chords = {
            # key of C
            ("C", "C"): ["C", "E", "G"],
            ("Caug", "C"): ["C", "E", "G#"],
            ("Csus2", "C"): ["C", "D", "G"],
            ("Csus4", "C"): ["C", "F", "G"],
            ("C6", "C"): ["C", "E", "G", "A"],
            ("C7", "C"): ["C", "E", "G", "A#"],  # FIXME: A# should be Bb
            ("C9", "C"): ["C", "E", "G", "A#", "D"],  # FIXME: A# should be Bb
            ("Cmaj7", "C"): ["C", "E", "G", "B"],
            ("Cmaj9", "C"): ["C", "E", "G", "B", "D"],
            ("Cm6", "C"): ["C", "D#", "G", "A"],  # FIXME: D# should be Eb
            ("Cm7", "C"): [
                "C",
                "D#",
                "G",
                "A#",
            ],  # FIXME: D# should be Eb, A# should be Bb
            ("Caug7", "C"): ["C", "E", "G#", "A#"],  # FIXME: A# should be Bb
            ("Cm9", "C"): [
                "C",
                "D#",
                "G",
                "A#",
                "D",
            ],  # FIXME: D# should be Eb, A# should be Bb
            ("C7b9", "C"): [
                "C",
                "E",
                "G",
                "A#",
                "C#",
            ],  # FIXME: A# should be Bb, C# should be Db
            ("Dm", "C"): ["D", "F", "A"],
            ("Bdim", "C"): ["B", "D", "F"],
            # key of C#
            ("C#", "C#"): ["C#", "E#", "G#"],
            ("C#7", "C#"): ["C#", "E#", "G#", "B"],
            # key of e
            ("B/A", "e"): ["A", "B", "D#", "F#"],
        }
        for (chord, key), notes in chords.items():
            with self.subTest(chord=chord, key=key):
                self.assertEqual(chord_name_to_note_names(chord, key), notes)

    def test_chord_name_to_pitches(self) -> None:
        chords = {
            "C/B": [11, 0, 4, 7],
            "C": [0, 4, 7],
            "Cm": [0, 3, 7],
            "Cdim": [0, 3, 6],
            "C6": [0, 4, 7, 9],
            "C7": [0, 4, 7, 10],
            "Cmaj7": [0, 4, 7, 11],
            "Cm6": [0, 3, 7, 9],
            "Cm7": [0, 3, 7, 10],
            "Cdim7": [0, 3, 6, 9],
        }
        key = "C"
        for name, pitches in chords.items():
            with self.subTest(name=name, key=key):
                self.assertEqual(chord_name_to_pitches(name), pitches)
                self.assertEqual(chord_name_from_pitches(pitches, key), name)
