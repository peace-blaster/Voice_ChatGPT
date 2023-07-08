from setuptools import setup, find_packages

setup(
    name='speech2gpt',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple python app that records voice, transcribes it to text using Google Speech-to-Text API, sends it to GPT-4 API, and converts the response to speech.',
    packages=find_packages(), 
    install_requires=[
        'sounddevice>=0.4.1',
        'numpy>=1.25.0',
        'scipy>=1.1.0',
        'openai>=0.27.0',
        'transformers>=4.30.2',
        'torchaudio>=0.9.0',
        'torch>=1.9.0',
        'pyaudio>=0.2.13',
        'pyttsx3>=2.90',
        'pyttsx4>=1.1' # for Mac support
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
