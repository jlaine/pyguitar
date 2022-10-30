import unittest

from pyguitar.chords import (
    chord_name_from_pitches,
    chord_name_from_roman,
    chord_name_to_note_names,
    chord_name_to_pitches,
)


class ChordsTest(unittest.TestCase):
    def test_chord_name_from_roman(self):
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

    def test_chord_name_from_roman_minor_key(self):
        chords = {
            "I": "E",
            "II": "F#",
            "III": "G",
            "IV": "A",
            "V": "B",
            "VI": "C",
            "VII": "D",
            "VIIdim": "Ddim",
            "viidim": "Ddim",
        }
        for roman, name in chords.items():
            with self.subTest(roman=roman):
                self.assertEqual(chord_name_from_roman(roman, "e"), name)

    def test_chord_name_to_note_names(self):
        chords = {
            # key of C
            ("C", "C"): ["C", "E", "G"],
            ("Caug", "C"): ["C", "E", "Ab"],  # FIXME : Ab should be G#
            ("Csus2", "C"): ["C", "D", "G"],
            ("Csus4", "C"): ["C", "F", "G"],
            ("Dm", "C"): ["D", "F", "A"],
            ("Bdim", "C"): ["B", "D", "F"],
            # key of C#
            ("C#", "C#"): ["C#", "E#", "G#"],
            # key of e
            ("B/A", "e"): ["A", "B", "D#", "F#"],
        }
        for (chord, key), notes in chords.items():
            with self.subTest(chord=chord, key=key):
                self.assertEqual(chord_name_to_note_names(chord, key), notes)

    def test_chord_name_to_pitches(self):
        chords = {
            "C/B": [11, 0, 4, 7],
            "C": [0, 4, 7],
            "Cm": [0, 3, 7],
            "Cdim": [0, 3, 6],
            "C7": [0, 4, 7, 10],
            "Cmaj7": [0, 4, 7, 11],
            "Cm7": [0, 3, 7, 10],
            "Cdim7": [0, 3, 6, 9],
        }
        for name, pitches in chords.items():
            with self.subTest(chord=name):
                self.assertEqual(chord_name_to_pitches(name), pitches)
                self.assertEqual(chord_name_from_pitches(pitches, "C"), name)
