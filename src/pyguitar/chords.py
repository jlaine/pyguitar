import dataclasses
import functools
import re

from pyguitar.notes import (
    MAJOR_SCALE,
    NOTE_ALPHABET,
    ROMAN_ALPHABET,
    augment,
    diminish,
    key_name_to_note_names,
    note_name_from_roman,
    note_name_to_pitch,
    parse_note_alteration,
    shift,
)


@dataclasses.dataclass
class Quality:
    notation: str
    intervals: tuple[str, ...]
    description: str

    @functools.cached_property
    def pitches(self) -> list[int]:
        return [_get_interval_pitch(i) for i in self.intervals]


CHORD_QUALITIES = {
    quality.notation: quality
    for quality in [
        # 3 notes
        Quality("", ("1", "3", "5"), "major triad"),
        Quality("m", ("1", "b3", "5"), "minor triad"),
        Quality("aug", ("1", "3", "#5"), "augmented triad"),
        Quality("dim", ("1", "b3", "b5"), "diminished triad"),
        Quality("sus2", ("1", "2", "5"), "suspended second"),
        Quality("sus4", ("1", "4", "5"), "suspended fourth"),
        # 4 notes
        Quality("6", ("1", "3", "5", "6"), "major sixth"),
        Quality("m6", ("1", "b3", "5", "6"), "minor sixth"),
        Quality("7", ("1", "3", "5", "b7"), "dominant seventh"),
        Quality("7b5", ("1", "3", "b5", "b7"), "dominant seventh flat five"),
        Quality("maj7", ("1", "3", "5", "7"), "major seventh"),
        Quality("m7", ("1", "b3", "5", "b7"), "minor seventh"),
        Quality("m7b5", ("1", "b3", "b5", "b7"), "minor seventh flat five"),
        Quality("mmaj7", ("1", "b3", "5", "7"), "minor major seventh"),
        Quality("aug7", ("1", "3", "#5", "b7"), "augmented seventh"),
        Quality("augmaj7", ("1", "3", "#5", "7"), "augmented major seventh"),
        Quality("dim7", ("1", "b3", "b5", "bb7"), "diminished seventh"),
        Quality("dimmaj7", ("1", "b3", "b5", "7"), "diminished major seventh"),
        Quality("add4", ("1", "3", "4", "5"), "major add fourth"),
        Quality("madd4", ("1", "b3", "4", "5"), "minor add fourth"),
        Quality("add9", ("1", "3", "4", "9"), "major add ninth"),
        Quality("madd9", ("1", "b3", "4", "9"), "minor add ninth"),
        # 5 notes
        Quality("9", ("1", "3", "5", "b7", "9"), "dominant ninth"),
        Quality("maj9", ("1", "3", "5", "7", "9"), "major ninth"),
        Quality("m9", ("1", "b3", "5", "b7", "9"), "minor ninth"),
        Quality("7b9", ("1", "3", "5", "b7", "b9"), "dominant seventh flat nine"),
        # 6 notes
        Quality("11", ("1", "3", "5", "b7", "9", "11"), "dominant eleventh"),
        Quality("7#11", ("1", "3", "5", "b7", "9", "#11"), "dominant sharp eleventh"),
        Quality("maj11", ("1", "3", "5", "7", "9", "11"), "major eleventh"),
        Quality("m11", ("1", "b3", "5", "b7", "9", "11"), "minor eleventh"),
    ]
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


def _parse_chord_name(name: str, alphabet: list[str]) -> tuple[str, Quality, str]:
    alphabet_re = "(?:" + ("|".join(alphabet)) + ")[b#]?"
    quality_re = "|".join(CHORD_QUALITIES.keys())
    chord_re = re.compile(
        "^(" + alphabet_re + ")(" + quality_re + ")(?:/(" + alphabet_re + "))?$"
    )
    m = chord_re.match(name)
    if not m:
        raise ValueError("Could not parse chord notation %s" % name)
    root = m.group(1)
    quality = CHORD_QUALITIES[m.group(2)]
    over = m.group(3)
    return root, quality, over


def chord_name_from_roman(roman: str, key: str) -> str:
    """
    Return a chord name for the given `roman` chord notation in the specified `key`.
    """
    numeral, quality, over = _parse_chord_name(roman, ROMAN_ALPHABET)
    numeral, alteration = parse_note_alteration(numeral)

    # get root
    minor = numeral.islower()
    chord = note_name_from_roman(numeral, key) + alteration
    if minor and quality.notation != "dim":
        chord += "m"
    chord += quality.notation

    # bass
    if over:
        chord += "/" + note_name_from_roman(over, key)

    return chord


def chord_name_to_description(chord: str) -> str:
    """
    Return a textual description for the given `chord`.
    """
    root_name, quality, over = _parse_chord_name(chord, NOTE_ALPHABET)
    description = f"{root_name} {quality.description}"
    if over:
        description += f" over {over}"
    return description


def chord_name_to_pitches(chord: str) -> list[int]:
    """
    Return the pitches to play the specified `chord`.
    """
    root_name, quality, over = _parse_chord_name(chord, NOTE_ALPHABET)
    root_pitch = note_name_to_pitch(root_name)

    pitches = shift(root_pitch, quality.pitches)
    if over:
        over_pitch = note_name_to_pitch(over)
        if over_pitch >= root_pitch:
            over_pitch -= 12
        pitches.insert(0, over_pitch)

    return pitches


def chord_name_to_interval_names(chord: str) -> list[str]:
    """
    Return the interval names for the specified `chord`.
    """
    root_name, quality, over = _parse_chord_name(chord, NOTE_ALPHABET)
    assert not over, "Slash chords are not supported"
    return list(quality.intervals)


def chord_name_to_note_names(chord: str) -> list[str]:
    """
    Return the note names to play the specified `chord`.
    """
    root_name, quality, over = _parse_chord_name(chord, NOTE_ALPHABET)
    names = [
        _apply_interval_to_note(root_name, interval) for interval in quality.intervals
    ]
    if over:
        names.insert(0, over)
    return names
