from typing import Sequence


class Note:
    C2 = 36
    D2 = 38
    E2 = 40
    F2 = 41
    G2 = 43
    A2 = 45
    B2 = 47

    C3 = 48
    D3 = 50
    E3 = 52
    F3 = 53
    G3 = 55
    A3 = 57
    B3 = 59

    C4 = 60
    D4 = 62
    E4 = 64
    F4 = 65
    G4 = 67
    A4 = 69
    B4 = 71


NOTE_ALPHABET = ["C", "D", "E", "F", "G", "A", "B"]
NOTE_NAMES = (
    ("C", "B#"),  # major/minor scale cannot start with B#
    ("C#", "Db"),  # minor scale cannot start with Db
    ("D",),
    ("Eb", "D#"),  # major scale cannot start with D#
    ("E", "Fb"),  # major/minor scale cannot start with Fb
    ("F", "E#"),  # major/minor scale cannot start with E#
    ("F#", "Gb"),  # minor scale cannot start with Gb
    ("G",),
    ("Ab", "G#"),  # major scale cannot start with G#
    ("A",),
    ("Bb", "A#"),  # major scale cannot start with A#
    ("B", "Cb"),  # minor scale cannot start with Cb
)

# Roman numerals.
ROMAN_NUMERALS_LOWER = ["i", "ii", "iii", "iv", "v", "vi", "vii"]
ROMAN_NUMERALS_UPPER = [num.upper() for num in ROMAN_NUMERALS_LOWER]
ROMAN_ALPHABET = ROMAN_NUMERALS_LOWER + ROMAN_NUMERALS_UPPER

# Scales.
MAJOR_SCALE = (0, 2, 4, 5, 7, 9, 11)
MAJOR_SCALE_ROMAN = ("I", "ii", "iii", "IV", "V", "vi", "viidim")
MINOR_SCALE = (0, 2, 3, 5, 7, 8, 10)
MINOR_SCALE_ROMAN = ("i", "iidim", "III", "iv", "v", "VI", "VII")
SCALE_NAMES = {
    tuple(MAJOR_SCALE): "major",
    tuple(MINOR_SCALE): "minor",
}


class Namer:
    def __init__(self, root: int) -> None:
        self._note_names = {}
        for pitches in [MAJOR_SCALE, MINOR_SCALE]:
            scale = shift(root, pitches)
            names = scale_note_names(scale)
            for i, note in enumerate(scale):
                self._note_names[note % 12] = names[i]

    def name_note(self, note: int) -> str:
        return self._note_names[note % 12]


def shift(root: int, pitches: Sequence[int]) -> list[int]:
    return [root + x for x in pitches]


def unshift(notes: Sequence[int]) -> tuple[int, list[int]]:
    root = notes[0]
    return root, [x - root for x in notes]


def key_note_names(key: str) -> list[str]:
    """
    Return the list of note names in the given `key`.
    """
    root_name = key_root_name(key)
    root_pitch = note_name_to_pitch(root_name)
    minor = key.islower()
    pitches = shift(root_pitch, MINOR_SCALE if minor else MAJOR_SCALE)
    return [note_name_from_pitch(p, key) for p in pitches]


def key_root_name(key: str) -> str:
    return key[0].upper() + key[1:]


def note_name_from_pitch(pitch: int, key: str) -> str:
    """
    Return the note name for the given `pitch` in the specified `key`.
    """
    namer = Namer(note_name_to_pitch(key_root_name(key)))
    return namer.name_note(pitch)


def note_name_from_roman(roman: str, key: str) -> str:
    """
    Return the note name for the given `roman` numeral in the specified `key`.
    """
    index = ROMAN_NUMERALS_LOWER.index(roman.lower())
    notes = key_note_names(key)
    return notes[index]


def note_name_to_pitch(note: str) -> int:
    """
    Return the pitch to play the specified `note`.
    """
    for value, names in enumerate(NOTE_NAMES):
        if note in names:
            return value
    raise ValueError("Unknown note %s" % note)


def prettify(note: str) -> str:
    return note.replace("b", "♭").replace("#", "♯")


def prettify_chord(chord: str) -> str:
    return prettify(chord).replace("dim", "°")


def prettify_key(key: str) -> str:
    kind = "minor" if key.islower() else "major"
    return prettify(key_root_name(key)) + " " + kind


def scale_note_names(scale):
    root_name = NOTE_NAMES[scale[0] % 12][0]
    note_index = NOTE_ALPHABET.index(root_name[0])

    note_names = [root_name]
    for note in scale[1:]:
        note_index = (note_index + 1) % 7
        for name in NOTE_NAMES[note % 12]:
            if name[0] == NOTE_ALPHABET[note_index]:
                note_names.append(name)
                break
    if len(note_names) != len(scale):
        raise ValueError("Scale cannot start with %s" % root_name)
    return note_names
