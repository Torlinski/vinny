"""Microphone Stream object"""
# pylint: disable=unused-argument
from typing import Generator, Optional

import pyaudio
from six.moves import queue


class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    DEFAULT_RATE = 16000

    def __init__(
        self,
        rate: Optional[int] = DEFAULT_RATE,
        chunk: Optional[int] = DEFAULT_RATE,
    ):
        self._rate = rate
        self._chunk = chunk

        self._buff = queue.Queue()
        self.closed = True
        self.transcript = ''
        self._audio_interface = None
        self._audio_stream = None

    def __enter__(self):
        """Initiate stream"""
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(
        self, type, value, traceback
    ):   # pylint: disable=redefined-builtin
        """Exit Stream"""
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self) -> Generator[bytes, None, None]:
        """Provides generator for transcription chunks"""
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
