import unittest

from pyguitar.notes import prettify


class NotesTest(unittest.TestCase):
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
