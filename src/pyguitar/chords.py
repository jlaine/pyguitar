import re

from pyguitar.notes import (
    NOTE_ALPHABET,
    ROMAN_ALPHABET,
    note_name_from_pitch,
    note_name_from_roman,
    note_name_to_pitch,
    shift,
    unshift,
)

CHORD_QUALITY_TO_OFFSETS = {
    # triads
    "": (0, 4, 7),
    "m": (0, 3, 7),
    "aug": (0, 4, 8),
    "dim": (0, 3, 6),
    # suspended chords
    "sus2": (0, 2, 7),
    "sus4": (0, 5, 7),
    # seventh chords
    "7": (0, 4, 7, 10),
    "maj7": (0, 4, 7, 11),
    "m7": (0, 3, 7, 10),
    "dim7": (0, 3, 6, 9),
    # ninth chords
    "9": (0, 4, 7, 10, 14),  # dominant ninth
    "maj9": (0, 4, 7, 11, 14),  # major ninth
    "m9": (0, 3, 7, 10, 14),  # minor ninth
    "7b9": (0, 4, 7, 10, 13),  # dominant minor ninth
}
CHORD_OFFSETS_TO_QUALITY = dict(
    (tuple(v), k) for (k, v) in CHORD_QUALITY_TO_OFFSETS.items()
)


def parse_chord_name(name: str, alphabet: list[str]) -> tuple[str, str, str]:
    alphabet_re = "(?:" + ("|".join(alphabet)) + ")[b#]?"
    quality_re = "|".join(CHORD_QUALITY_TO_OFFSETS.keys())
    chord_re = re.compile(
        "^(" + alphabet_re + ")(" + quality_re + ")(?:/(" + alphabet_re + "))?$"
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
    try:
        root, offsets = unshift(pitches)
        quality = CHORD_OFFSETS_TO_QUALITY[tuple(offsets)]
        return note_name_from_pitch(root, key) + quality
    except KeyError:
        root, offsets = unshift(pitches[1:])
        quality = CHORD_OFFSETS_TO_QUALITY[tuple(offsets)]
        return (
            note_name_from_pitch(root, key)
            + quality
            + "/"
            + note_name_from_pitch(pitches[0], key)
        )


def chord_name_from_roman(roman: str, key: str) -> str:
    """
    Return a chord name for the given `roman` chord notation in the specified `key`.
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
    root_pitch = note_name_to_pitch(root_name)

    pitches = shift(root_pitch, CHORD_QUALITY_TO_OFFSETS[quality])
    if over:
        pitches.insert(0, note_name_to_pitch(over))

    return pitches


def chord_name_to_note_names(chord: str, key: str) -> list[str]:
    """
    Return the note names to play the specified `chord`.
    """
    pitches = chord_name_to_pitches(chord)
    return [note_name_from_pitch(p, key) for p in pitches]
