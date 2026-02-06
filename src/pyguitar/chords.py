import re

from pyguitar.notes import (
    MAJOR_SCALE,
    NOTE_ALPHABET,
    ROMAN_ALPHABET,
    augment,
    diminish,
    key_name_to_note_names,
    note_name_from_pitch,
    note_name_from_roman,
    note_name_to_pitch,
    parse_note_alteration,
    shift,
    unshift,
)

CHORD_QUALITY_TO_INTERVAL_NAMES = {
    # triads
    "": ("1", "3", "5"),
    "m": ("1", "b3", "5"),
    "aug": ("1", "3", "#5"),
    "dim": ("1", "b3", "b5"),
    # suspended chords
    "sus2": ("1", "2", "5"),
    "sus4": ("1", "4", "5"),
    # sixth chords
    "6": ("1", "3", "5", "6"),
    "m6": ("1", "b3", "5", "6"),
    # seventh chords
    "7": ("1", "3", "5", "b7"),  # dominant seventh
    "maj7": ("1", "3", "5", "7"),  # major seventh
    "m7": ("1", "b3", "5", "b7"),  # minor seventh
    "m7b5": ("1", "b3", "b5", "b7"),  # minor seventh flat five
    "mmaj7": ("1", "b3", "5", "7"),  # minor major seventh
    "aug7": ("1", "3", "#5", "b7"),  # augmented seventh
    "augmaj7": ("1", "3", "#5", "7"),  # augmented major seventh
    "dim7": ("1", "b3", "b5", "bb7"),  # diminished seventh
    # ninth chords
    "9": ("1", "3", "5", "b7", "9"),  # dominant ninth
    "maj9": ("1", "3", "5", "7", "9"),  # major ninth
    "m9": ("1", "b3", "5", "b7", "9"),  # minor ninth
    "7b9": ("1", "3", "5", "b7", "b9"),  # dominant minor ninth
}


def _apply_interval_to_note(root: str, interval: str) -> str:
    alterations, offset = _parse_interval(interval)

    # Apply the interval and alteration.
    notes_in_key = key_name_to_note_names(root)
    note = notes_in_key[offset % 7]
    for alteration in alterations:
        if alteration == "#":
            note = augment(note)
        else:
            note = diminish(note)
    return note


def _get_interval_pitch(interval: str) -> int:
    alterations, offset = _parse_interval(interval)

    value = MAJOR_SCALE[offset % 7] + 12 * (offset // 7)
    for alteration in alterations:
        if alteration == "#":
            value += 1
        else:
            value -= 1
    return value


def _parse_interval(interval: str) -> tuple[str, int]:
    m = re.match(r"^([b#]*)(\d+)$", interval)
    assert m, f"Invalid interval {interval}"
    alterations = m.group(1)
    offset = int(m.group(2)) - 1
    return alterations, offset


CHORD_QUALITY_TO_OFFSETS = {
    k: tuple(_get_interval_pitch(i) for i in v)
    for (k, v) in CHORD_QUALITY_TO_INTERVAL_NAMES.items()
}
CHORD_OFFSETS_TO_QUALITY = {v: k for (k, v) in CHORD_QUALITY_TO_OFFSETS.items()}


def _parse_chord_name(name: str, alphabet: list[str]) -> tuple[str, str, str]:
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
    numeral, quality, over = _parse_chord_name(roman, ROMAN_ALPHABET)
    numeral, alteration = parse_note_alteration(numeral)

    # get root
    minor = numeral.islower()
    chord = note_name_from_roman(numeral, key) + alteration
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
    root_name, quality, over = _parse_chord_name(chord, NOTE_ALPHABET)
    root_pitch = note_name_to_pitch(root_name)

    pitches = shift(root_pitch, CHORD_QUALITY_TO_OFFSETS[quality])
    if over:
        pitches.insert(0, note_name_to_pitch(over))

    return pitches


def chord_name_to_note_names(chord: str) -> list[str]:
    """
    Return the note names to play the specified `chord`.
    """
    root_name, quality, over = _parse_chord_name(chord, NOTE_ALPHABET)
    names = [
        _apply_interval_to_note(root_name, interval)
        for interval in CHORD_QUALITY_TO_INTERVAL_NAMES[quality]
    ]
    if over:
        names.insert(0, over)
    return names
