"""
This is code straight copy pasted from ChatGPT

"""
import pyaudio
import json
from vosk import Model, KaldiRecognizer

# Path to the Vosk model directory
model_path = "models/vosk-model-small-en-in-0.4"

# Load the model
model = Model(model_path)

# Initialize the recognizer with the model and the sample rate
recognizer = KaldiRecognizer(model, 16000)

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open a stream for audio input
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("Listening...")

try:
    data = bytes()
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        # print(data)
        # print(type(data))
        # exit(0)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            print(result_dict.get("text", ""))
            data = bytes()
        else:
            partial_result = recognizer.PartialResult()
            partial_result_dict = json.loads(partial_result)
            print("Partial result:", partial_result_dict.get("partial", ""))

except KeyboardInterrupt:
    print("Stopping transcription...")

finally:
    # Clean up: stop and close the stream and terminate the PyAudio object
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("Finished.")

