# main.py
import os
from google.cloud import speech
import stt.transcription as transcription
from server.client import Client
from process import CommandProcessor
from STT_Session import STT_Session
import os

def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'dependable-fuze-388619-8912b19e9733.json'

    language_code = "en-US"  # a BCP-47 language tag

    socket_client = Client('http://localhost:8080')
    socket_client.update_status('Ready')

    speech_client = speech.SpeechClient()
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
            responses = speech_client.streaming_recognize(streaming_config, requests)
            session = STT_Session()
            os.system('cls' if os.name=='nt' else 'clear')
            print("Started listening...")
            socket_client.update_status('Listening')

            for response in responses:
                for result in response.results:
                    transcript = result.alternatives[0].transcript
                    session.update(transcript)
                    socket_client.update_para(session.get_text())
                    socket_client.update_comlist(session.get_comlist())

        except KeyboardInterrupt as e:
            print("Ended Stream")
        except Exception as e:
            if not isinstance(e, KeyboardInterrupt):
                print(e)



if __name__ == "__main__":
    main()
