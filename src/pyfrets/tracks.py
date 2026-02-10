import dataclasses
from fractions import Fraction

import mido


@dataclasses.dataclass
class TrackNote:
    duration: Fraction
    pitch: int


class Track:
    def __init__(self, beats_per_minute: int):
        self._beats_per_minute = beats_per_minute
        self._chords: list[list[TrackNote]] = []

    def add_notes(self, pitches: list[int], duration: Fraction) -> None:
        self._chords.append(
            [TrackNote(duration=duration, pitch=pitch) for pitch in pitches]
        )

    def to_midi(self, beat_time: int = 480) -> mido.MidiTrack:
        midi_track = mido.MidiTrack()
        midi_track.append(
            mido.MetaMessage(
                "set_tempo", tempo=mido.bpm2tempo(self._beats_per_minute), time=0
            )
        )
        midi_track.append(mido.Message("program_change", program=26, time=0))
        for chord in self._chords:
            for note in chord:
                midi_track.append(mido.Message("note_on", note=note.pitch, time=0))
            for idx, note in enumerate(chord):
                midi_track.append(
                    mido.Message(
                        "note_off",
                        note=note.pitch,
                        time=0 if idx else int(beat_time * note.duration),
                    )
                )
        return midi_track
