# This file will play a local audio file
print('This is playaudio.py')

import os
#from playsound import playsound
import pygame

# start pygame mixer
pygame.mixer.init()

# get directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
audio_file = os.path.join(script_dir, "golden_parody.mp3")

# load and play audio
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play()

# if user input, stop
input()
pygame.mixer.music.stop()
