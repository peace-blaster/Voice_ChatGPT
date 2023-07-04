import logging
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write  
import openai
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torchaudio
import torch
import os
import pyttsx3

class VoiceChatGPT:
    def __init__(self):
        self.logger = logging.getLogger()
        logging.basicConfig(level=logging.INFO)
        self.recording = None
        self.transcription = None
        self.response = None
        self.load_openai_key()
        self.log_default_audio_device()

    def load_openai_key(self):
        try:
            with open("openai_key", "r") as file:
                openai.api_key = file.read().strip()
            self.logger.info("OpenAI key loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load OpenAI key: {e}")

    def log_default_audio_device(self):
        default_devices = sd.default.device
        default_input_device_info = sd.query_devices(default_devices[0])
        self.logger.info(f"Default input device: {default_input_device_info['name']}")

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
            return True
        except Exception as e:
            self.logger.error(f"Failed to save audio file: {e}")
            return False

    def convert_speech_to_text(self, filepath):
        print('is this even running?')
        self.logger.info("Converting speech to text...")
        try:
            # Load the pre-trained model and processor
            processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
            model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

            # Load audio
            speech, rate = torchaudio.load(filepath)

            # If stereo, convert to mono
            self.logger.info("Converting audio to mono...")
            if speech.shape[0] > 1:
                speech = speech.mean(dim=0, keepdim=True)

            # Resample the audio to 16kHz
            self.logger.info("Resampling to 16kHz...")
            if rate != 16000:
                resampler = torchaudio.transforms.Resample(orig_freq=rate, new_freq=16000)
                speech = resampler(speech)
                rate = 16000

            self.logger.info(f"Shape of the speech tensor: {speech.shape}")
            self.logger.info(f"Rate: {rate}")

            # Preprocess the audio
            self.logger.info("Preprocessing audio...")
            speech = speech.squeeze()
            input_values = processor(speech, sampling_rate=rate, return_tensors="pt").input_values

            # Perform speech-to-text
            self.logger.info("Converting to text...")
            logits = model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)

            # Convert the predicted IDs to text
            transcription = processor.decode(predicted_ids[0])
            self.logger.info(f"Raw transcription: {transcription}")
            transcription = transcription.lower()
            self.logger.info(f"Processed transcription: {transcription}")
            return transcription
        except Exception as e:
            self.logger.error(f"Failed to convert speech to text: {e}")
            return None


    def get_response_from_gpt(self):
        self.logger.info("Getting response from ChatGPT...")
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=self.transcription,
                max_tokens=60
            )
            self.response = response.choices[0].text.strip()
            self.logger.info(f"ChatGPT Response: {self.response}")
            print(f'ChatGPT: {self.response}')
        except Exception as e:
            self.logger.error(f"Failed to get response from ChatGPT: {e}")

    def text_to_speech(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def run(self):
        self.record_audio()
        if self.recording is not None:
            if self.save_audio():
                self.transcription = self.convert_speech_to_text('recording.wav')
                if self.transcription is not None:
                    self.get_response_from_gpt()
                    if self.response is not None:
                        #os.remove("recording.wav")
                        self.text_to_speech(self.response)
                        return self.response
        return None
                