#!/bin/bash

# Update Homebrew (This is the package manager for macOS, similar to dnf on Fedora)
brew update

# Install non-python dependencies
brew install portaudio ffmpeg python@3.11 # nsss should be included by default for Mac