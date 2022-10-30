import re

from pyguitar.notes import (
    DIMINISHED_7TH,
    DIMINISHED_TRIAD,
    DOMINANT_7TH,
    MAJOR_7TH,
    MAJOR_TRIAD,
    MINOR_7TH,
    MINOR_TRIAD,
    NOTE_ALPHABET,
    Namer,
    key_note_names,
    note_name_to_int,
    shift,
)

# roman numerals
ROMAN_NUMERALS_LOWER = ["i", "ii", "iii", "iv", "v", "vi", "vii"]
ROMAN_NUMERALS_UPPER = [num.upper() for num in ROMAN_NUMERALS_LOWER]


def parse_chord_name(name: str, alphabet: str) -> tuple[str, str, str]:
    alphabet_re = "|".join(alphabet)
    chord_re = re.compile(
        "^(" + alphabet_re + ")(|m|°|dim|7|maj7|m7|dim7)(?:/(" + alphabet_re + "))?$"
    )
    m = chord_re.match(name)
    if not m:
        raise ValueError("Could not parse chord notation %s" % name)
    root = m.group(1)
    quality = m.group(2).replace("°", "dim")
    assert quality in ("", "m", "dim", "7", "m7", "maj7", "dim7"), (
        "Unknown quality %s" % quality
    )
    over = m.group(3)
    return root, quality, over


def chord_name_from_roman(roman: str, key: str) -> str:
    """
    Convert a `roman` chord notation to a chord name in the specified `key`.
    """
    numeral, quality, over = parse_chord_name(
        roman, ROMAN_NUMERALS_LOWER + ROMAN_NUMERALS_UPPER
    )

    # get root
    minor = numeral.islower()
    chord = note_name_from_roman(numeral, key)
    if minor and quality != "dim":
        chord += "m"
    chord += quality

    # bass
    if over:
        chord += "/" + note_name_from_roman(over, key)

    return chord


def chord_name_to_pitches(chord: str) -> list[int]:
    """
    Return the pitches to play the specified `chord`.
    """
    root_name, quality, over = parse_chord_name(chord, NOTE_ALPHABET)
    root = note_name_to_int(root_name)
    if quality == "":
        pitches = shift(root, MAJOR_TRIAD)
    elif quality == "m":
        pitches = shift(root, MINOR_TRIAD)
    elif quality == "dim":
        pitches = shift(root, DIMINISHED_TRIAD)
    elif quality == "7":
        pitches = shift(root, DOMINANT_7TH)
    elif quality == "maj7":
        pitches = shift(root, MAJOR_7TH)
    elif quality == "m7":
        pitches = shift(root, MINOR_7TH)
    elif quality == "dim7":
        pitches = shift(root, DIMINISHED_7TH)
    else:
        raise ValueError("Unhandled chord quality '%s'" % quality)
    return pitches


def chord_name_to_note_names(chord: str, key: str) -> list[int]:
    """
    Return the note names to play the specified `chord`.
    """
    pitches = chord_name_to_pitches(chord)
    namer = Namer(note_name_to_int(key.upper()))
    return [namer.name_note(p) for p in pitches]


def note_name_from_roman(roman: str, key: str) -> str:
    """
    Convert a `roman` numeral to a note in the specifiied `key`.
    """
    index = ROMAN_NUMERALS_LOWER.index(roman.lower())
    notes = key_note_names(key)
    return notes[index]
