from gtts import gTTS
import playsound
import os

x = ['sunny', 'sagar', 'akhil']
tts = 'tts'
for i in range(0,3):
    tts = gTTS(text= x[i], lang = 'en')
    file1 = str("hello" + str(i) + ".mp3")
    tts.save(file1)
    playsound.playsound(file1,True)
    os.remove(file1)