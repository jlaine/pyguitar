import unittest

from pyguitar.notes import (
    key_name_to_note_names,
    note_name_from_pitch,
    note_name_from_roman,
    note_name_to_pitch,
    prettify_chord,
    prettify_key,
    prettify_note,
)


class NotesTest(unittest.TestCase):
    def test_key_name_to_note_names(self):
        keys = {
            # Major scales.
            "Cb": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],
            "Gb": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
            "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
            "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
            "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
            "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
            "F": ["F", "G", "A", "Bb", "C", "D", "E"],
            "C": ["C", "D", "E", "F", "G", "A", "B"],
            "G": ["G", "A", "B", "C", "D", "E", "F#"],
            "D": ["D", "E", "F#", "G", "A", "B", "C#"],
            "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
            "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
            "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
            "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
            "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
            # Minor scales.
            "eb": ["Eb", "F", "Gb", "Ab", "Bb", "Cb", "Db"],
            "bb": ["Bb", "C", "Db", "Eb", "F", "Gb", "Ab"],
            "f": ["F", "G", "Ab", "Bb", "C", "Db", "Eb"],
            "c": ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
            "g": ["G", "A", "Bb", "C", "D", "Eb", "F"],
            "d": ["D", "E", "F", "G", "A", "Bb", "C"],
            "a": ["A", "B", "C", "D", "E", "F", "G"],
            "e": ["E", "F#", "G", "A", "B", "C", "D"],
            "b": ["B", "C#", "D", "E", "F#", "G", "A"],
            "f#": ["F#", "G#", "A", "B", "C#", "D", "E"],
            "c#": ["C#", "D#", "E", "F#", "G#", "A", "B"],
            "g#": ["G#", "A#", "B", "C#", "D#", "E", "F#"],
            "d#": ["D#", "E#", "F#", "G#", "A#", "B", "C#"],
        }
        for key, names in keys.items():
            with self.subTest(key=key):
                self.assertEqual(key_name_to_note_names(key), names)

        # Invalid scale.
        with self.assertRaises(ValueError) as cm:
            key_name_to_note_names("B#")
        self.assertEqual(str(cm.exception), "Scale cannot start with B#")

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

    def test_note_name_to_pitch(self):
        notes = {
            "C": 0,
            "C#": 1,
            "D": 2,
            "D#": 3,
            "E": 4,
            "F": 5,
            "G": 7,
            "G#": 8,
            "A": 9,
            "A#": 10,
            "B": 11,
        }
        key = "C"
        for name, pitch in notes.items():
            with self.subTest(name=name, key=key):
                self.assertEqual(note_name_to_pitch(name), pitch)
                self.assertEqual(note_name_from_pitch(pitch, key), name)

        with self.assertRaises(ValueError):
            note_name_to_pitch("X")

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

    def test_prettify_note(self):
        notes = {
            "C": "C",
            "Cb": "C♭",
            "C#": "C♯",
        }
        for plain, pretty in notes.items():
            with self.subTest(plain=plain):
                self.assertEqual(prettify_note(plain), pretty)
