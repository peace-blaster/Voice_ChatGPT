#!/bin/bash

# Update system
sudo dnf update -y

# Install non-python dependencies
sudo dnf install -y portaudio ffmpeg-free espeak