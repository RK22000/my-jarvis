#!/bin/bash
# Run from project root dir
# Ends in project root dir
mkdir -p models/vosk
cd models/vosk/
wget https://alphacephei.com/vosk/models/vosk-model-small-en-in-0.4.zip
unzip vosk-model-small-en-in-0.4.zip
rm vosk-model-small-en-in-0.4.zip
cd ../..
