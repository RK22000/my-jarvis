"""
This is code straight copy pasted from ChatGPT

"""
import pyaudio
import json
from vosk import Model, KaldiRecognizer
import logging

log_file = "stt.log"
logging.basicConfig(filename=log_file, level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_STT():

    print(f"Logging at {log_file}")
    # Path to the Vosk model directory
    model_path = "models/vosk/vosk-model-small-en-in-0.4"

    logger.info(f"Loading model: {model_path}")
    # Load the model
    model = Model(model_path)

    logger.info(f"Initializing KaldiRecognizer")
    # Initialize the recognizer with the model and the sample rate
    recognizer = KaldiRecognizer(model, 16000)

    logger.info(f"Initializing PyAudio")
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    logger.info("Opeining an audio stream")
    # Open a stream for audio input
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    logger.info("Listening...")

    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_dict = json.loads(result)
                yield result_dict
            else:
                partial_result = recognizer.PartialResult()
                partial_result_dict = json.loads(partial_result)
                yield partial_result_dict

    except KeyboardInterrupt:
        logger.info("Stopping transcription...")
        raise StopIteration()

    finally:
        # Clean up: stop and close the stream and terminate the PyAudio object
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Finished.")

