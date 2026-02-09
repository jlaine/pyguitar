import functools
from typing import Sequence, cast


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
NOTE_NAMES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_NAMES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
NOTE_PITCHES = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}

# Roman numerals.
ROMAN_NUMERALS_LOWER = ["i", "ii", "iii", "iv", "v", "vi", "vii"]
ROMAN_NUMERALS_UPPER = [num.upper() for num in ROMAN_NUMERALS_LOWER]
ROMAN_ALPHABET = ROMAN_NUMERALS_LOWER + ROMAN_NUMERALS_UPPER

# Scales.
MAJOR_SCALE = (0, 2, 4, 5, 7, 9, 11)
MAJOR_SCALE_ROMAN = ("I", "ii", "iii", "IV", "V", "vi", "viidim")
MINOR_SCALE = (0, 2, 3, 5, 7, 8, 10)
MINOR_SCALE_ROMAN = ("i", "iidim", "III", "iv", "v", "VI", "VII")

# Circle of fifths.
KEYS = [
    ("Cb", "ab"),
    ("Gb", "eb"),
    ("Db", "bb"),
    ("Ab", "f"),
    ("Eb", "c"),
    ("Bb", "g"),
    ("F", "d"),
    ("C", "a"),  # no alterations
    ("G", "e"),
    ("D", "b"),
    ("A", "f#"),
    ("E", "c#"),
    ("B", "g#"),
    ("F#", "d#"),
    ("C#", "a#"),
]
KEY_INDEXES = [(f + 7) % len(KEYS) for f in range(len(KEYS))]
KEY_SIGNATURES = {}
MAJOR_KEYS = [KEYS[i][0] for i in KEY_INDEXES if KEYS[i][0] is not None]
MINOR_KEYS = cast(
    list[str], [KEYS[i][1] for i in KEY_INDEXES if KEYS[i][1] is not None]
)  # mypy does not detect this list will only contain strings.
for idx, (major, minor) in enumerate(KEYS):
    if major is not None:
        KEY_SIGNATURES[major] = idx - 7
    if minor is not None:
        KEY_SIGNATURES[minor] = idx - 7


def shift(root: int, pitches: Sequence[int]) -> list[int]:
    return [root + x for x in pitches]


@functools.lru_cache()
def build_note_names(key: str) -> list[str]:
    root_name = key_root_name(key)
    root_pitch = note_name_to_pitch(root_name)
    note_index = NOTE_ALPHABET.index(root_name[0])
    offsets = MINOR_SCALE if key.islower() else MAJOR_SCALE

    if KEY_SIGNATURES.get(key, 0) < 0 or len(key) > 1 and key[1] == "b":
        alter = diminish
        note_alphabet = NOTE_NAMES_FLAT
    else:
        alter = augment
        note_alphabet = NOTE_NAMES_SHARP

    # Name notes in the key.
    all_note_names = [""] * 12
    all_note_names[root_pitch % 12] = root_name
    for offset in offsets[1:]:
        note_index = (note_index + 1) % 7
        note_pitch = (root_pitch + offset) % 12

        # Find the accidental to match the pitch.
        note_name = NOTE_ALPHABET[note_index]
        for i in range(3):
            if note_name_to_pitch(note_name) == note_pitch:
                all_note_names[note_pitch % 12] = note_name
                break
            note_name = alter(note_name)
        else:
            raise ValueError(f"Scale {key} requires too many accidentals")

    # Fill the gaps.
    for note_pitch, val in enumerate(all_note_names):
        if not val:
            all_note_names[note_pitch] = note_alphabet[note_pitch]

    return all_note_names


def augment(note: str) -> str:
    """
    Augment the given note.
    """
    if note.endswith("b"):
        return note[:-1]
    else:
        return note + "#"


def diminish(note: str) -> str:
    """
    Diminish the given note.
    """
    if note.endswith("#"):
        return note[:-1]
    else:
        return note + "b"


def key_name_to_note_names(key: str) -> list[str]:
    """
    Return the list of note names in the given `key`.
    """
    return [note_name_from_pitch(p, key) for p in key_name_to_pitches(key)]


def key_name_to_pitches(key: str) -> list[int]:
    """
    Return the list of pitches in the given `key`.
    """
    root_name = key_root_name(key)
    root_pitch = note_name_to_pitch(root_name)
    minor = key.islower()
    return shift(root_pitch, MINOR_SCALE if minor else MAJOR_SCALE)


def key_root_name(key: str) -> str:
    return key[0].upper() + key[1:]


def note_name_from_pitch(pitch: int, key: str) -> str:
    """
    Return the note name for the given `pitch` in the specified `key`.
    """
    note_names = build_note_names(key)
    return note_names[pitch % 12]


def note_name_from_roman(roman: str, key: str) -> str:
    """
    Return the note name for the given `roman` numeral in the specified `key`.
    """
    numeral, alteration = parse_note_alteration(roman)
    index = ROMAN_NUMERALS_LOWER.index(numeral.lower())
    notes = key_name_to_note_names(key)
    return notes[index] + alteration


def note_name_to_pitch(note: str) -> int:
    """
    Return the pitch to play the specified `note`.
    """
    try:
        pitch = NOTE_PITCHES[note[0]]
    except KeyError:
        raise ValueError("Unknown note %s" % note)
    for alteration in note[1:]:
        if alteration == "b":
            pitch -= 1
        else:
            pitch += 1
    return pitch % 12


def parse_note_alteration(note: str) -> tuple[str, str]:
    alteration = ""
    while note.endswith("#") or note.endswith("b"):
        alteration = note[-1] + alteration
        note = note[:-1]
    return note, alteration


def prettify_chord(chord: str) -> str:
    return prettify_note(chord).replace("dim", "°")


def prettify_key(key: str) -> str:
    kind = "minor" if key.islower() else "major"
    return prettify_note(key_root_name(key)) + " " + kind


def prettify_note(note: str) -> str:
    return (
        note.replace("bb", "𝄫").replace("##", "𝄪").replace("b", "♭").replace("#", "♯")
    )
