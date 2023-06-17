import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from google.cloud import speech_v1p1beta1 as speech
import io
import os

# Set the duration and sample rate
duration = 3  # seconds
sample_rate = 16000  # Hz

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'dependable-fuze-388619-8912b19e9733.json'

# Record audio for the duration
print("Start speaking!")
myrecording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
sd.wait()  # Wait for the recording to finish

print("Recording finished!")

# Save the recording to a WAV file
write("output.wav", sample_rate, myrecording)

# Transcribe the WAV file using Google Speech-to-Text
def transcribe_audio_file():
    client = speech.SpeechClient()

    with io.open("output.wav", "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

transcribe_audio_file()
