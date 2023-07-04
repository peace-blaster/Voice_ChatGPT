import logging
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write  
import openai
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torchaudio
import torch
import os

class VoiceChatGPT:
    def __init__(self):
        self.logger = logging.getLogger()
        logging.basicConfig(level=logging.INFO)
        self.recording = None
        self.transcription = None
        self.response = None
        self.load_openai_key()

    def load_openai_key(self):
        try:
            with open("openai_key", "r") as file:
                openai.api_key = file.read().strip()
            self.logger.info("OpenAI key loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load OpenAI key: {e}")

    def record_audio(self, duration=10):
        try:
            self.logger.info("Recording audio...")
            self.recording = sd.rec(int(duration * 44100), samplerate=44100, channels=2)
            sd.wait()
            self.logger.info("Audio recording successful")
        except Exception as e:
            self.logger.error(f"Failed to record audio: {e}")

    def save_audio(self):
        try:
            write('recording.wav', 44100, self.recording)  # use scipy's write instead of sd.write
            self.logger.info("Audio file saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save audio file: {e}")

    def convert_speech_to_text(self, filepath):
        try:
            # Load the pre-trained model and processor
            processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
            model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

            # Load audio
            speech, rate = torchaudio.load(filepath)

            # If stereo, convert to mono
            if speech.shape[0] > 1:
                speech = speech.mean(dim=0, keepdim=True)

            # Resample the audio to 16kHz
            if rate != 16000:
                resampler = torchaudio.transforms.Resample(orig_freq=rate, new_freq=16000)
                speech = resampler(speech)
                rate = 16000

            # Preprocess the audio
            input_values = processor(speech, sampling_rate=rate, return_tensors="pt").input_values

            # Perform speech-to-text
            logits = model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)

            # Convert the predicted IDs to text
            self.transcription = processor.decode(predicted_ids[0])
            self.logger.info(f"Transcribed text: {self.transcription}")
        except Exception as e:
            self.logger.error(f"Failed to convert speech to text: {e}")

    def get_response_from_gpt(self):
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=self.transcription,
                max_tokens=60
            )
            self.response = response.choices[0].text.strip()
            self.logger.info(f"ChatGPT Response: {self.response}")
        except Exception as e:
            self.logger.error(f"Failed to get response from ChatGPT: {e}")

    def run(self):
        self.record_audio()
        if self.recording is not None:
            if self.save_audio():
                self.convert_speech_to_text('recording.wav')
                if self.transcription is not None:
                    self.get_response_from_gpt()
                    if self.response is not None:
                        os.remove("recording.wav")
                        return self.response
        return None

                