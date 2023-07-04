# Voice_ChatGPT
PoC to use voice to communicate with ChatGPT

## Usage
- Run `python main.py`
- Speak when you see `INFO:root:Recording audio...`
- Await response

## Setup:
- Ensure the mic you want to use is the default for your OS
- Install non-pip dependencies (for connecting to audio devices on your system):
  - RHEL-based Linux:
    - `./fedora_setup.sh`
- Install pip dependencies (you may want to make a `venv` first): `pip install .`
- Put OpenAI token in root folder of repo as `openai_key` (don't worry, it's in `.gitignore`)

## Notes:
- Will use default input and output audio devices
- Only tested on Linux Fedora so far, Mac is next
