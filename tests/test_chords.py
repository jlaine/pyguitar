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
            # triads
            "C": ["C", "E", "G"],
            "Cm": ["C", "Eb", "G"],
            "Caug": ["C", "E", "G#"],
            "Cdim": ["C", "Eb", "Gb"],
            # suspended chords
            "Csus2": ["C", "D", "G"],
            "Csus4": ["C", "F", "G"],
            # sixth chords
            "C6": ["C", "E", "G", "A"],
            "Cm6": ["C", "Eb", "G", "A"],
            # seventh chords
            "C7": ["C", "E", "G", "Bb"],
            "Cmaj7": ["C", "E", "G", "B"],
            "Cm7": ["C", "Eb", "G", "Bb"],
            "Cm7b5": ["C", "Eb", "Gb", "Bb"],
            "Cmmaj7": ["C", "Eb", "G", "B"],
            "Caug7": ["C", "E", "G#", "Bb"],
            "Caugmaj7": ["C", "E", "G#", "B"],
            "Cdim7": ["C", "Eb", "Gb", "Bbb"],
            # ninth chords
            "C9": ["C", "E", "G", "Bb", "D"],
            "Cmaj9": ["C", "E", "G", "B", "D"],
            "Cm9": ["C", "Eb", "G", "Bb", "D"],
            "C7b9": ["C", "E", "G", "Bb", "Db"],
            # other
            "C#": ["C#", "E#", "G#"],
            "C#7": ["C#", "E#", "G#", "B"],
            "B/A": ["A", "B", "D#", "F#"],
        }
        for chord, notes in chords.items():
            with self.subTest(chord=chord):
                self.assertEqual(chord_name_to_note_names(chord), notes)

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
