import dataclasses
import unittest

from pyfrets.chords import (
    chord_name_from_roman,
    chord_name_to_description,
    chord_name_to_interval_names,
    chord_name_to_note_names,
    chord_name_to_pitches,
)


@dataclasses.dataclass
class ChordInfo:
    description: str
    notes: list[str]
    pitches: list[int]


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

    def test_chords(self) -> None:
        chords = {
            # 3 notes
            "C": ChordInfo(
                description="C major triad",
                notes=["C", "E", "G"],
                pitches=[0, 4, 7],
            ),
            "Cm": ChordInfo(
                description="C minor triad",
                notes=["C", "Eb", "G"],
                pitches=[0, 3, 7],
            ),
            "Caug": ChordInfo(
                description="C augmented triad",
                notes=["C", "E", "G#"],
                pitches=[0, 4, 8],
            ),
            "Cdim": ChordInfo(
                description="C diminished triad",
                notes=["C", "Eb", "Gb"],
                pitches=[0, 3, 6],
            ),
            "Csus2": ChordInfo(
                description="C suspended second",
                notes=["C", "D", "G"],
                pitches=[0, 2, 7],
            ),
            "Csus4": ChordInfo(
                description="C suspended fourth",
                notes=["C", "F", "G"],
                pitches=[0, 5, 7],
            ),
            # 4 notes
            "C6": ChordInfo(
                description="C major sixth",
                notes=["C", "E", "G", "A"],
                pitches=[0, 4, 7, 9],
            ),
            "Cm6": ChordInfo(
                description="C minor sixth",
                notes=["C", "Eb", "G", "A"],
                pitches=[0, 3, 7, 9],
            ),
            "C7": ChordInfo(
                description="C dominant seventh",
                notes=["C", "E", "G", "Bb"],
                pitches=[0, 4, 7, 10],
            ),
            "C7b5": ChordInfo(
                description="C dominant seventh flat five",
                notes=["C", "E", "Gb", "Bb"],
                pitches=[0, 4, 6, 10],
            ),
            "Cmaj7": ChordInfo(
                description="C major seventh",
                notes=["C", "E", "G", "B"],
                pitches=[0, 4, 7, 11],
            ),
            "Cm7": ChordInfo(
                description="C minor seventh",
                notes=["C", "Eb", "G", "Bb"],
                pitches=[0, 3, 7, 10],
            ),
            "Cm7b5": ChordInfo(
                description="C minor seventh flat five",
                notes=["C", "Eb", "Gb", "Bb"],
                pitches=[0, 3, 6, 10],
            ),
            "Cmmaj7": ChordInfo(
                description="C minor major seventh",
                notes=["C", "Eb", "G", "B"],
                pitches=[0, 3, 7, 11],
            ),
            "Caug7": ChordInfo(
                description="C augmented seventh",
                notes=["C", "E", "G#", "Bb"],
                pitches=[0, 4, 8, 10],
            ),
            "Caugmaj7": ChordInfo(
                description="C augmented major seventh",
                notes=["C", "E", "G#", "B"],
                pitches=[0, 4, 8, 11],
            ),
            "Cdim7": ChordInfo(
                description="C diminished seventh",
                notes=["C", "Eb", "Gb", "Bbb"],
                pitches=[0, 3, 6, 9],
            ),
            "Cdimmaj7": ChordInfo(
                description="C diminished major seventh",
                notes=["C", "Eb", "Gb", "B"],
                pitches=[0, 3, 6, 11],
            ),
            "Cadd4": ChordInfo(
                description="C major add fourth",
                notes=["C", "E", "F", "G"],
                pitches=[0, 4, 5, 7],
            ),
            "Cmadd4": ChordInfo(
                description="C minor add fourth",
                notes=["C", "Eb", "F", "G"],
                pitches=[0, 3, 5, 7],
            ),
            "Cadd9": ChordInfo(
                description="C major add ninth",
                notes=["C", "E", "F", "D"],
                pitches=[0, 4, 5, 14],
            ),
            "Cmadd9": ChordInfo(
                description="C minor add ninth",
                notes=["C", "Eb", "F", "D"],
                pitches=[0, 3, 5, 14],
            ),
            # 5 notes
            "C9": ChordInfo(
                description="C dominant ninth",
                notes=["C", "E", "G", "Bb", "D"],
                pitches=[0, 4, 7, 10, 14],
            ),
            "Cmaj9": ChordInfo(
                description="C major ninth",
                notes=["C", "E", "G", "B", "D"],
                pitches=[0, 4, 7, 11, 14],
            ),
            "Cm9": ChordInfo(
                description="C minor ninth",
                notes=["C", "Eb", "G", "Bb", "D"],
                pitches=[0, 3, 7, 10, 14],
            ),
            "C7b9": ChordInfo(
                description="C dominant seventh flat nine",
                notes=["C", "E", "G", "Bb", "Db"],
                pitches=[0, 4, 7, 10, 13],
            ),
            # 6 notes
            "C11": ChordInfo(
                description="C dominant eleventh",
                notes=["C", "E", "G", "Bb", "D", "F"],
                pitches=[0, 4, 7, 10, 14, 17],
            ),
            "C7#11": ChordInfo(
                description="C dominant sharp eleventh",
                notes=["C", "E", "G", "Bb", "D", "F#"],
                pitches=[0, 4, 7, 10, 14, 18],
            ),
            "Cmaj11": ChordInfo(
                description="C major eleventh",
                notes=["C", "E", "G", "B", "D", "F"],
                pitches=[0, 4, 7, 11, 14, 17],
            ),
            "Cm11": ChordInfo(
                description="C minor eleventh",
                notes=["C", "Eb", "G", "Bb", "D", "F"],
                pitches=[0, 3, 7, 10, 14, 17],
            ),
            # other
            "Abm": ChordInfo(
                description="Ab minor triad",
                notes=["Ab", "Cb", "Eb"],
                pitches=[8, 11, 15],
            ),
            "B/A": ChordInfo(
                description="B major triad over A",
                notes=["A", "B", "D#", "F#"],
                pitches=[9, 11, 15, 18],
            ),
            "C/B": ChordInfo(
                description="C major triad over B",
                notes=["B", "C", "E", "G"],
                pitches=[-1, 0, 4, 7],
            ),
            "Cbm": ChordInfo(
                description="Cb minor triad",
                notes=["Cb", "Ebb", "Gb"],
                pitches=[11, 14, 18],
            ),
            "C#": ChordInfo(
                description="C# major triad",
                notes=["C#", "E#", "G#"],
                pitches=[1, 5, 8],
            ),
            "C#7": ChordInfo(
                description="C# dominant seventh",
                notes=["C#", "E#", "G#", "B"],
                pitches=[1, 5, 8, 11],
            ),
            "D/C": ChordInfo(
                description="D major triad over C",
                notes=["C", "D", "F#", "A"],
                pitches=[0, 2, 6, 9],
            ),
            "Dm7b5": ChordInfo(
                description="D minor seventh flat five",
                notes=["D", "F", "Ab", "C"],
                pitches=[2, 5, 8, 12],
            ),
            "E#": ChordInfo(
                description="E# major triad",
                notes=["E#", "G##", "B#"],
                pitches=[5, 9, 12],
            ),
            "Fbm": ChordInfo(
                description="Fb minor triad",
                notes=["Fb", "Abb", "Cb"],
                pitches=[4, 7, 11],
            ),
            "Gm7": ChordInfo(
                description="G minor seventh",
                notes=["G", "Bb", "D", "F"],
                pitches=[7, 10, 14, 17],
            ),
        }
        for name, info in chords.items():
            with self.subTest(name=name):
                self.assertEqual(chord_name_to_description(name), info.description)
                self.assertEqual(chord_name_to_note_names(name), info.notes)
                self.assertEqual(chord_name_to_pitches(name), info.pitches)

    def test_chord_name_to_interval_names(self) -> None:
        self.assertEqual(chord_name_to_interval_names("C"), ["1", "3", "5"])
