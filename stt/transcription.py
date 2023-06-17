import pyaudio
from six.moves import queue

# Audio recording parameters
RATE = 16000
#CHUNK = int(RATE / 10)  # 100ms
CHUNK = RATE

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        self._buff = queue.Queue()
        self.closed = True
        self.transcript = ""

    def __enter__(self):
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

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
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

            yield b"".join(data)


class Document(object):
    def __init__(self):
        self.contents = ""

    def add_to_document(self, text):
        self.contents += text

    def listen_print_loop(self, responses):
        """Iterates through server responses and prints them."""

        for response in responses:
            if not response.results:
                continue

            result = response.results[0]

            if not result.alternatives:
                continue

            if result.is_final:
                self.add_to_document(result.alternatives[0].transcript)
                print('Transcript: {}'.format(result.alternatives[0].transcript))
            #print(f"Transcript: {result.alternatives[0].transcript} (confidence: {result.alternatives[0].confidence})")