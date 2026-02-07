import io
import unittest
from fractions import Fraction

import mido

from pyguitar.tracks import Track, TrackNote


class TracksTest(unittest.TestCase):
    def test_add_notes(self) -> None:
        track = Track(beats_per_minute=100)
        track.add_notes([48], duration=Fraction(1, 4))
        self.assertEqual(
            track._chords,
            [
                [TrackNote(duration=Fraction(1, 4), pitch=48)],
            ],
        )

    def test_to_midi(self) -> None:
        track = Track(beats_per_minute=100)
        track.add_notes([48], duration=Fraction(1, 4))
        buffer = io.BytesIO()

        midi_file = mido.MidiFile()
        midi_file.tracks.append(track.to_midi())
        midi_file.save(file=buffer)

        self.assertEqual(
            buffer.getvalue(),
            bytes.fromhex(
                "4d546864000000060001000101e04d54726b0000001600ff51030927c000c01a009030407880304000ff2f00"
            ),
        )
