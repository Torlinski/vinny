import pyaudio
import audioop
import time

# Set the duration and sample rate
RATE = 16000  # Hz
CHUNK = int(RATE/2)  # Process half a second of audio at a time

def start_monitoring():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    while True:
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)  # width=2 for format=paInt16
        print(f"RMS: {rms}")
        time.sleep(0.5)  # Sleep for half a second

    stream.stop_stream()
    stream.close()
    p.terminate()

start_monitoring()
