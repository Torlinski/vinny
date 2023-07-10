"""main entry point for transcription"""
import logging
import os
import traceback

from google.cloud import speech

from src.core.MicrophoneStream import MicrophoneStream
from src.core.SIOServer import SIOServer

logging.basicConfig(level=logging.DEBUG)

def main(socketio):
    """Run transcription stream and create session"""
    os.system('cls' if os.name == 'nt' else 'clear')
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    print(files)
    os.environ[
        'GOOGLE_APPLICATION_CREDENTIALS'
    ] = 'dependable-fuze-388619-8912b19e9733.json'
    language_code = 'en-US'  # a BCP-47 language tag
    speech_client = speech.SpeechClient()
    speech_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=MicrophoneStream.DEFAULT_RATE,
        language_code=language_code,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=speech_config,
        interim_results=False,
    )

    stt_server = SIOServer(socketio)
    stt_server.set_status('Ready')

    try:
        with MicrophoneStream() as stream:

            audio_generator = stream.generator()

            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )

            responses = speech_client.streaming_recognize(
                streaming_config, requests
            )
            logging.debug('Started listening...')
            stt_server.set_status('Listening')

            for response in responses:
                for result in response.results:
                    transcript = result.alternatives[0].transcript
                    try:
                        stt_server.update(transcript)
                    except Exception as e:
                        stt_server.set_status('Internal Error')
                        logging.debug(e)

    except KeyboardInterrupt:
        logging.debug('Manually Ended Stream')
    except Exception as e:
        if not isinstance(e, KeyboardInterrupt):
            traceback.print_exc()
            logging.debug(e)