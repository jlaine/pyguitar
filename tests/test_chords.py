import unittest

from pyguitar.chords import chord_name_from_roman, chord_name_to_pitches


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
            "VII°": "Bdim",
            "VIIdim": "Bdim",
            "I7": "C7",
            "IVmaj7": "Fmaj7",
            "IV/I": "F/C",
        }
        for roman, name in chords.items():
            with self.subTest(roman=roman):
                self.assertEqual(chord_name_from_roman(roman, "C"), name)

    def test_chord_name_from_roman_minor_key(self):
        chords = {
            "I": "E",
            "II": "F#",
            "III": "G",
            "IV": "A",
            "V": "B",
            "VI": "C",
            "VII": "D",
            "VII°": "Ddim",
            "vii°": "Ddim",
        }
        for roman, name in chords.items():
            with self.subTest(roman=roman):
                self.assertEqual(chord_name_from_roman(roman, "e"), name)

    def test_chord_name_to_pitches(self):
        chords = {
            "C": [0, 4, 7],
            "Cm": [0, 3, 7],
            "Cdim": [0, 3, 6],
            "C7": [0, 4, 7, 10],
            "Cmaj7": [0, 4, 7, 11],
            "Cm7": [0, 3, 7, 10],
        }
        for name, pitches in chords.items():
            with self.subTest(chord=name):
                self.assertEqual(chord_name_to_pitches(name), pitches)
