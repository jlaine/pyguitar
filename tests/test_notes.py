import unittest

from pyguitar.notes import key_note_names, prettify


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

    def test_prettify(self):
        notes = {
            "C": "C",
            "Cb": "C♭",
            "C#": "C♯",
            "Cdim": "C°",
        }
        for plain, pretty in notes.items():
            with self.subTest(plain=plain):
                self.assertEqual(prettify(plain), pretty)
