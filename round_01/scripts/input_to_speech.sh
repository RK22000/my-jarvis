#!/usr/bin/env bash
./piper/piper --model models/piper/en_GB-semaine-medium.onnx --output-raw |   aplay -r 22050 -f S16_LE -t raw -
