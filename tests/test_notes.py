import unittest

from pyguitar.notes import (
    key_note_names,
    note_name_from_roman,
    note_name_to_int,
    prettify,
    prettify_chord,
    prettify_key,
)


class NotesTest(unittest.TestCase):
    def test_key_note_names(self):
        keys = {
            "C": ["C", "D", "E", "F", "G", "A", "B"],
            "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
            "D": ["D", "E", "F#", "G", "A", "B", "C#"],
            "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
            # "D#": invalid!
            "c": ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
            "c#": ["C#", "D#", "E", "F#", "G#", "A", "B"],
            "d": ["D", "E", "F", "G", "A", "Bb", "C"],
            "eb": ["Eb", "F", "Gb", "Ab", "Bb", "Cb", "Db"],
        }
        for key, names in keys.items():
            with self.subTest(key=key):
                self.assertEqual(key_note_names(key), names)

    def test_note_name_from_roman(self):
        notes = {
            "I": "C",
            "II": "D",
            "III": "E",
            "IV": "F",
            "V": "G",
            "VI": "A",
            "VII": "B",
        }
        for roman, name in notes.items():
            with self.subTest(roman=roman):
                self.assertEqual(note_name_from_roman(roman, "C"), name)

    def test_note_name_to_int(self):
        notes = {
            "C": 0,
            "Db": 1,
            "D": 2,
            "Eb": 3,
            "E": 4,
            "F": 5,
            "G": 7,
            "Ab": 8,
            "A": 9,
            "Bb": 10,
            "B": 11,
        }
        for name, pitch in notes.items():
            with self.subTest(name=name):
                self.assertEqual(note_name_to_int(name), pitch)

        with self.assertRaises(ValueError):
            note_name_to_int("X")

    def test_prettify(self):
        notes = {
            "C": "C",
            "Cb": "C♭",
            "C#": "C♯",
        }
        for plain, pretty in notes.items():
            with self.subTest(plain=plain):
                self.assertEqual(prettify(plain), pretty)

    def test_prettify_chord(self):
        notes = {
            "C": "C",
            "Cm": "Cm",
            "Cb": "C♭",
            "Cbm": "C♭m",
            "C#": "C♯",
            "Cdim": "C°",
        }
        for plain, pretty in notes.items():
            with self.subTest(plain=plain):
                self.assertEqual(prettify_chord(plain), pretty)

    def test_prettify_key(self):
        notes = {
            "C": "C major",
            "Cb": "C♭ major",
            "C#": "C♯ major",
            "c": "C minor",
            "cb": "C♭ minor",
            "c#": "C♯ minor",
        }
        for plain, pretty in notes.items():
            with self.subTest(plain=plain):
                self.assertEqual(prettify_key(plain), pretty)
