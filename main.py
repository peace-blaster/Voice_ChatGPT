import logging
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write  
import openai

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

try:
    with open("openai_key", "r") as file:
        openai.api_key = file.read().strip()
    logger.info("OpenAI key loaded successfully")
except Exception as e:
    logger.error(f"Failed to load OpenAI key: {e}")

def main():
    duration = 10  # seconds
    try:
        logger.info("Recording audio...")
        recording = sd.rec(int(duration * 44100), samplerate=44100, channels=2)
        sd.wait()
        logger.info("Audio recording successful")
    except Exception as e:
        logger.error(f"Failed to record audio: {e}")
        return

    try:
        write('recording.wav', 44100, recording)  # use scipy's write instead of sd.write
        logger.info("Audio file saved successfully")
    except Exception as e:
        logger.error(f"Failed to save audio file: {e}")
        return

    # Put your Speech-to-Text conversion code here, and assume the resulting text is in the 'text' variable.

    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=text,
            max_tokens=60
        )
        result_text = response.choices[0].text.strip()
        logger.info(f"ChatGPT Response: {result_text}")
    except Exception as e:
        logger.error(f"Failed to get response from ChatGPT: {e}")

if __name__ == "__main__":
    main()
