#!/bin/bash
brew update
brew install portaudio ffmpeg python@3.9 llvm # nsss should be included by default for Mac

# Set llvm-config path
export LLVM_CONFIG=$(which llvm-config)
