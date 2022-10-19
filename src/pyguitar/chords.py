import re

from mingus.core import keys

# roman numerals
ROMAN_NUMERALS_LOWER = ["i", "ii", "iii", "iv", "v", "vi", "vii"]
ROMAN_NUMERALS_UPPER = [num.upper() for num in ROMAN_NUMERALS_LOWER]
ROMAN_CHORD_REGEX = re.compile("^([iv]+|[IV]+)(|°|dim|7|maj7)(?:/([iv]+|[IV]+))?$")


def note_roman_to_name(numeral: str, key: str) -> str:
    """
    Convert a roman `numeral` to a note in the specific `key`.
    """
    index = ROMAN_NUMERALS_LOWER.index(numeral.lower())
    notes = keys.get_notes(key)
    return notes[index]


def roman_to_name(chord: str, key: str) -> str:
    m = ROMAN_CHORD_REGEX.match(chord)
    if not m:
        raise ValueError("Could not parse roman notation chord %s" % chord)

    # get root
    numeral = m.group(1)
    minor = numeral == numeral.lower()
    note = note_roman_to_name(numeral, key)

    # get quality
    if minor:
        note += "m"

    quality = m.group(2)
    if quality == "":
        chord = note
    elif quality in ("°", "dim"):
        chord = note + "dim"
    elif quality in ("maj7", "7"):
        chord = note + quality
    else:
        raise ValueError()

    # bass
    if m.group(3):
        chord += "/" + note_roman_to_name(m.group(3), key)

    return chord
