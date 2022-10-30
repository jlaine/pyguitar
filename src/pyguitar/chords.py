import re

from pyguitar.notes import (
    NOTE_ALPHABET,
    ROMAN_ALPHABET,
    Namer,
    key_root_name,
    note_name_from_roman,
    note_name_to_int,
    shift,
    unshift,
)

CHORD_QUALITY_TO_OFFSETS = {
    # triads
    "": (0, 4, 7),
    "m": (0, 3, 7),
    "dim": (0, 3, 6),
    # seventh chords
    "7": (0, 4, 7, 10),
    "maj7": (0, 4, 7, 11),
    "m7": (0, 3, 7, 10),
    "dim7": (0, 3, 6, 9),
}
CHORD_OFFSETS_TO_QUALITY = dict(
    (tuple(v), k) for (k, v) in CHORD_QUALITY_TO_OFFSETS.items()
)


def parse_chord_name(name: str, alphabet: str) -> tuple[str, str, str]:
    alphabet_re = "(?:" + ("|".join(alphabet)) + ")[b#]?"
    chord_re = re.compile(
        "^(" + alphabet_re + ")(|m|dim|7|maj7|m7|dim7)(?:/(" + alphabet_re + "))?$"
    )
    m = chord_re.match(name)
    if not m:
        raise ValueError("Could not parse chord notation %s" % name)
    root = m.group(1)
    quality = m.group(2)
    over = m.group(3)
    return root, quality, over


def chord_name_from_pitches(pitches: list[int], key: str) -> str:
    """
    Return a chord name for the given `pitches` in the specified `key`.
    """
    namer = Namer(note_name_to_int(key_root_name(key)))
    try:
        root, offsets = unshift(pitches)
        quality = CHORD_OFFSETS_TO_QUALITY[tuple(offsets)]
        return namer.name_note(root) + quality
    except KeyError:
        root, offsets = unshift(pitches[1:])
        quality = CHORD_OFFSETS_TO_QUALITY[tuple(offsets)]
        return namer.name_note(root) + quality + "/" + namer.name_note(pitches[0])


def chord_name_from_roman(roman: str, key: str) -> str:
    """
    Convert a `roman` chord notation to a chord name in the specified `key`.
    """
    numeral, quality, over = parse_chord_name(roman, ROMAN_ALPHABET)

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
    root_pitch = note_name_to_int(root_name)

    pitches = shift(root_pitch, CHORD_QUALITY_TO_OFFSETS[quality])
    if over:
        pitches.insert(0, note_name_to_int(over))

    return pitches


def chord_name_to_note_names(chord: str, key: str) -> list[int]:
    """
    Return the note names to play the specified `chord`.
    """
    pitches = chord_name_to_pitches(chord)
    namer = Namer(note_name_to_int(key_root_name(key)))
    return [namer.name_note(p) for p in pitches]
