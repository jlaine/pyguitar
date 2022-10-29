from typing import Dict, List, Sequence, Tuple


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
    ("C", "B♯"),  # major/minor scale cannot start with B♯
    ("C♯", "D♭"),  # minor scale cannot start with D♭
    ("D",),
    ("E♭", "D♯"),  # major scale cannot start with D♯
    ("E", "F♭"),  # major/minor scale cannot start with F♭
    ("F", "E♯"),  # major/minor scale cannot start with E♯
    ("F♯", "G♭"),  # minor scale cannot start with G♭
    ("G",),
    ("A♭", "G♯"),  # major scale cannot start with G♯
    ("A",),
    ("B♭", "A♯"),  # major scale cannot start with A♯
    ("B", "C♭"),  # minor scale cannot start with C♭
)

# scales
MAJOR_SCALE = (0, 2, 4, 5, 7, 9, 11)
MAJOR_SCALE_ROMAN = ("I", "ii", "iii", "IV", "V", "vi", "vii°")
MINOR_SCALE = (0, 2, 3, 5, 7, 8, 10)
MINOR_SCALE_ROMAN = ("i", "ii°", "III", "iv", "v", "VI", "VII")
SCALE_NAMES = {
    tuple(MAJOR_SCALE): "major",
    tuple(MINOR_SCALE): "minor",
}

# chords
DIMINISHED_TRIAD = (0, 3, 6)
DIMINISHED_7TH = (0, 3, 6, 9)
MAJOR_TRIAD = (0, 4, 7)
MAJOR_7TH = (0, 4, 7, 11)
DOMINANT_7TH = (0, 4, 7, 10)
MINOR_TRIAD = (0, 3, 7)
MINOR_7TH = (0, 3, 7, 10)
CHORD_NAMES = {
    tuple(MAJOR_TRIAD): "",
    tuple(MAJOR_7TH): "maj7",
    tuple(DOMINANT_7TH): "7",
    tuple(MINOR_TRIAD): "m",
    tuple(MINOR_7TH): "m7",
    tuple(DIMINISHED_TRIAD): "°",
    tuple(DIMINISHED_7TH): "°7",
}


class Namer:
    def __init__(self, root: int) -> None:
        self._note_names = {}
        for pitches in [MAJOR_SCALE, MINOR_SCALE]:
            scale = shift(root, pitches)
            names = scale_note_names(scale)
            for i, note in enumerate(scale):
                self._note_names[note % 12] = names[i]

    def name_chord(self, chord: Sequence[int]) -> str:
        root, pitches = unshift(chord)
        try:
            t = CHORD_NAMES[tuple(pitches)]
            return self.name_note(root) + t
        except KeyError:
            root, pitches = unshift(chord[1:])
            t = CHORD_NAMES[tuple(pitches)]
            return self.name_note(root) + t + "/" + self.name_note(chord[0])

    def name_note(self, note: int) -> str:
        return self._note_names[note % 12]

    def name_scale(self, scale: Sequence[int]) -> str:
        root, pitches = unshift(scale)
        t = SCALE_NAMES[tuple(pitches)]
        return self.name_note(scale[0]) + " " + t


def shift(root: int, pitches: Sequence[int]) -> List[int]:
    return [root + x for x in pitches]


def unshift(notes: Sequence[int]) -> Tuple[int, List[int]]:
    root = notes[0]
    return root, [x - root for x in notes]


def make_chords(
    scale: Sequence[int], roman: Sequence[str], sevenths: bool
) -> Dict[str, List[int]]:
    chords = {}
    for i, bit in enumerate(roman):
        if "°" in bit:
            chords[bit] = shift(scale[i], DIMINISHED_TRIAD)
            if sevenths:
                chords[bit + "7"] = shift(scale[i], DIMINISHED_7TH)
        elif bit == bit.upper():
            chords[bit] = shift(scale[i], MAJOR_TRIAD)
            if sevenths:
                chords[bit + "7"] = shift(scale[i], DOMINANT_7TH)
                chords[bit + "maj7"] = shift(scale[i], MAJOR_7TH)
        else:
            chords[bit] = shift(scale[i], MINOR_TRIAD)
            if sevenths:
                chords[bit + "7"] = shift(scale[i], MINOR_7TH)
    return chords


def note_name_to_int(name: str) -> int:
    for value, names in enumerate(NOTE_NAMES):
        if name in names:
            return value
    raise ValueError("Unknown note %s" % name)


def scale_chords(root: int, minor: bool, sevenths=True) -> Dict[str, List[int]]:
    if minor:
        scale = shift(root, MINOR_SCALE)
        return make_chords(scale, MINOR_SCALE_ROMAN, sevenths=sevenths)
    else:
        scale = shift(root, MAJOR_SCALE)
        return make_chords(scale, MAJOR_SCALE_ROMAN, sevenths=sevenths)


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
