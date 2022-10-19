import unittest

from pyguitar.chords import roman_to_name


class ChordsTest(unittest.TestCase):
    def test_roman_to_name_major_key(self):
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
                self.assertEqual(roman_to_name(roman, "C"), name)

    def test_roman_to_name_minor_key(self):
        chords = {
            "I": "E",
            "II": "F#",
            "III": "G",
            "IV": "A",
            "V": "B",
            "VI": "C",
            "VII": "D",
        }
        for roman, name in chords.items():
            with self.subTest(roman=roman):
                self.assertEqual(roman_to_name(roman, "e"), name)
