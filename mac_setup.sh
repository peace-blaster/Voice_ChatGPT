#!/bin/bash

# Update Homebrew (This is the package manager for macOS, similar to dnf on Fedora)
brew update

# Install non-python dependencies
brew install portaudio ffmpeg # nsss should be included by default for Mac