from gtts import gTTS
import pygame
pygame.mixer.init()

tts = gTTS('He served as the first Deputy Prime Minister of India. He was an Indian barrister, and a senior leader of the Indian National Congress who played a leading role in the country struggle for independence and guided its integration into a united, independent nation.[3] In India and elsewhere, he was often called Sardar', lang='en')
tts.save('hello.mp3')
file = "/home/pi/Desktop/hello.mp3"
pygame.mixer.music.load(file)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
