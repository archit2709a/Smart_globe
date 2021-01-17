import speech_recognition as sr
from os import path
import csv
import sys
import wikipedia
from google.cloud import texttospeech
import pygame
import requests
from bs4 import BeautifulSoup
import urllib.request as req
from pygame import mixer
import os
dir_path = '/home/pi/Images'
try:
    os.remove(dir_path)
    os.mkdir(dir_path)
except OSError as e:
    print("Error: %s : %s" % (dir_path, e.strerror))
    
 
GOOGLE_APPLICATION_CREDENTIALS="/home/pi/Downloads/Globe-47eb374a1236.json"
counter = 0
test_list = [ "//upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Increase2.svg/11px-Increase2.svg.png", "//upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Decrease2.svg/11px-Decrease2.svg.png", "//upload.wikimedia.org/wikipedia/commons/thumb/5/59/Increase_Negative.svg/11px-Increase_Negative.svg.png", '//upload.wikimedia.org/wikipedia/en/thumb/e/e7/Cscr-featured.svg/20px-Cscr-featured.svg.png', "//upload.wikimedia.org/wikipedia/en/thumb/8/8c/Extended-protection-shackle.svg/20px-Extended-protection-shackle.svg.png", "//upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Loudspeaker.svg/11px-Loudspeaker.svg.png", "//upload.wikimedia.org/wikipedia/en/thumb/1/1b/Semi-protection-shackle.svg/20px-Semi-protection-shackle.svg.png", "//upload.wikimedia.org/wikipedia/commons/thumb/4/47/Sound-icon.svg/20px-Sound-icon.svg.png", "//upload.wikimedia.org/wikipedia/en/thumb/f/f2/Edit-clear.svg/40px-Edit-clear.svg.png"]
pygame.mixer.init()
client = texttospeech.TextToSpeechClient()
mycsvlist = []
isCountryFound = False
with open("/home/pi/Desktop/world_country_and_usa_states_latitude_and_longitude_values.csv") as f:
    mycsv = csv.reader(f)
    mycsvlist = list(mycsv)

# obtain audio from the microphone
r = sr.Recognizer()
isbadAudio = True
# recognize speech using Sphinx
while isbadAudio:
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source,timeout=5, phrase_time_limit=5)
    # write audio to a WAV file
    with open("microphone-results.wav", "wb") as f:
        f.write(audio.get_wav_data())

    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "/home/pi/microphone-results.wav")

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the ent


    try:
        query = (r.recognize_google(audio))
        print(query)
        isbadAudio = False
    except sr.UnknownValueError:
        print("Could not understand audio")
        isCountryFound = True
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    if not isbadAudio:
        for index in range(1,len(mycsvlist)):
            if (query.lower() == mycsvlist[index][3].lower()):
                #print (index)
                print(mycsvlist[index][2] + ',' + mycsvlist[index][1]) 
                isCountryFound = True
                break
            if (not isCountryFound and index == len(mycsvlist)-1):
                isbadAudio = True
                print("0,0")
page = wikipedia.page(query)
wiki_text = wikipedia.summary(query, sentences=1)
print (wiki_text)
url = page.url
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
images = soup.find_all('img')
totalimages = min(len(images),20)
#for image in images:
for imageindex in range(0,totalimages):
    image = images[imageindex]
    counter = (counter + 1)
    str_value = str(counter)
    print(image['src'])
    if ((image['src']) in test_list): 
        print (".") 
    elif '//upload.wikimedia.org/wikipedia/commons/thumb/9/9a/' in (image['src']):
        break
    else:
        try:
            imgurl = ("https:" + image['src'])
            req.urlretrieve(imgurl, r"/home/pi/Images/image_name" + str_value + ".jpg")
        except:
            continue
input_text = texttospeech.SynthesisInput(text= wiki_text)


    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Standard-C",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

response = client.synthesize_speech(
    request={"input": input_text, "voice": voice, "audio_config": audio_config}
)

    # The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print('Audio content written to file "home/pi/output.mp3"')
file = "/home/pi/output.mp3"
mixer.init()
mixer.music.load(file)
mixer.music.play()
os.system('feh -Y -x -q -D 2 -B black -F -Z -z --on-last-slide quit -r /home/pi/Images')
