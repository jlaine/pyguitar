import typing

def bpm2tempo(bpm: int) -> int: ...

class BaseMessage: ...

class Message(BaseMessage):
    def __init__(self, type: str, **args: typing.Any) -> None: ...

class MetaMessage(BaseMessage):
    def __init__(self, type: str, **args: typing.Any) -> None: ...

class MidiFile:
    tracks: list[MidiTrack]

    def save(
        self, filename: str | None = None, file: typing.BinaryIO | None = None
    ) -> None: ...

class MidiTrack:
    def append(self, message: BaseMessage) -> None: ...
