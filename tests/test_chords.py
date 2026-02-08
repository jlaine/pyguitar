import unittest

from pyguitar.chords import (
    chord_name_from_pitches,
    chord_name_from_roman,
    chord_name_to_description,
    chord_name_to_interval_names,
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

    def test_chord_name_to_description(self) -> None:
        chords = {
            # 3 notes
            "C": "C major triad",
            "Cm": "C minor triad",
            "Caug": "C augmented triad",
            "Cdim": "C diminished triad",
            "Csus2": "C suspended second",
            "Csus4": "C suspended fourth",
            # 4 notes
            "C6": "C major sixth",
            "Cm6": "C minor sixth",
            "C7": "C dominant seventh",
            "C7b5": "C dominant seventh flat five",
            "Cmaj7": "C major seventh",
            "Cm7": "C minor seventh",
            "Cm7b5": "C minor seventh flat five",
            "Cmmaj7": "C minor major seventh",
            "Caug7": "C augmented seventh",
            "Caugmaj7": "C augmented major seventh",
            "Cdim7": "C diminished seventh",
            "Cdimmaj7": "C diminished major seventh",
            # 5 notes
            "C9": "C dominant ninth",
            "Cmaj9": "C major ninth",
            "Cm9": "C minor ninth",
            "C7b9": "C dominant seventh flat nine",
            # other
            "C/B": "C major triad over B",
        }
        for name, description in chords.items():
            with self.subTest(name=name):
                self.assertEqual(chord_name_to_description(name), description)

    def test_chord_name_to_interval_names(self) -> None:
        self.assertEqual(chord_name_to_interval_names("C"), ["1", "3", "5"])

    def test_chord_name_to_note_names(self) -> None:
        chords = {
            # 3 notes
            "C": ["C", "E", "G"],
            "Cm": ["C", "Eb", "G"],
            "Caug": ["C", "E", "G#"],
            "Cdim": ["C", "Eb", "Gb"],
            "Csus2": ["C", "D", "G"],
            "Csus4": ["C", "F", "G"],
            # 4 notes
            "C6": ["C", "E", "G", "A"],
            "Cm6": ["C", "Eb", "G", "A"],
            "C7": ["C", "E", "G", "Bb"],
            "C7b5": ["C", "E", "Gb", "Bb"],
            "Cmaj7": ["C", "E", "G", "B"],
            "Cm7": ["C", "Eb", "G", "Bb"],
            "Cm7b5": ["C", "Eb", "Gb", "Bb"],
            "Cmmaj7": ["C", "Eb", "G", "B"],
            "Caug7": ["C", "E", "G#", "Bb"],
            "Caugmaj7": ["C", "E", "G#", "B"],
            "Cdim7": ["C", "Eb", "Gb", "Bbb"],
            "Cdimmaj7": ["C", "Eb", "Gb", "B"],
            # 5 notes
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
            "D/C": [0, 2, 6, 9],
            "C/B": [-1, 0, 4, 7],
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
