# main.py
import os
from google.cloud import speech
import stt.transcription as transcription
from server.client import Client
from process import CommandProcessor

def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'dependable-fuze-388619-8912b19e9733.json'

    language_code = "en-US"  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=transcription.RATE,
        language_code=language_code,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=False,
    )

    with transcription.MicrophoneStream(transcription.RATE, transcription.CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        try:
            responses = client.streaming_recognize(streaming_config, requests)
        except Exception as e:
            print(e)

        client = Client('http://localhost:8080')
        processor = CommandProcessor(client)

        print("Started listening...")

        for response in responses:
            for result in response.results:
                transcript = result.alternatives[0].transcript
                print(transcript)
                processor.process(transcript)



if __name__ == "__main__":
    main()
