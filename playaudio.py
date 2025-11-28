# This file will play a local audio file
print('This is playaudio.py')

import os
from playsound import playsound

# get directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# build path to audio file relative to script
audio_file = os.path.join(script_dir, "golden_parody.mp3").replace("\\", "/")

# play audio
playsound(audio_file)
