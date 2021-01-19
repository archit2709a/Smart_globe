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
from time import sleep
import RPi.GPIO as GPIO
import shutil

shutil.rmtree('/home/pi/Images')
os.makedirs('/home/pi/Images')
file1 = open("/home/pi/Captions/image_name2.jpg.txt","w")#write mode 



GPIO.setmode(GPIO.BCM)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
pygame.init()
X = 1200
Y = 600
Motor1A = 2
Motor1B = 3

display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
#display_surface = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Show Text')
font = pygame.font.Font('freesansbold.ttf', 70)
text = font.render('Welcome...', True, black, white)
textRect = text.get_rect()
textRect.center = (X/4, Y / 2)
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)

while True:
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
            text = font.render('Say The Name of The Country', True, black, white)
            display_surface.fill(white)
            display_surface.blit(text, textRect)
            pygame.display.update()
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
            text = font.render("I Think You Said:" + r.recognize_google(audio), True, black, white)
            display_surface.fill(white)
            display_surface.blit(text, textRect)
            pygame.display.update()
            print(query)
            isbadAudio = False
        except sr.UnknownValueError:
            print("Could not understand audio")
            #isCountryFound = True
            isbadAudio = True
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        if not isbadAudio:
            if query == "India":
                wiki_text = "Home to one of the seven wonders of the world Taj Mahal, the Indian subcontinent is the seventh largest country of the world and stands apart from the rest of Asia separated by the Himalayas. The diverse country of 28 states and 8 union territories. The temperature is generally moderate. The country mainly consists of Hindus, whereas other religions such as Jainism, Sikhism, Christianity and Islamic also live in harmony."
                page = wikipedia.page(query)
            else:
                for index in range(1,len(mycsvlist)):
                    if (query.lower() == mycsvlist[index][3].lower()):
                        #print (index)
                        lat = (mycsvlist[index][1]) 
                        long = (mycsvlist[index][2])
                        print(lat + "," + long) 
                        isCountryFound = True
                        break
                    if (not isCountryFound and index == len(mycsvlist)-1):
                        isbadAudio = True
                        lat = ('0')
                        long = ('0')
                        print("0,0")
                    #rps = ('')
                    #time = (rps/360)
                    #GPIO.output(Motor1A,GPIO.HIGH) # to run motor in clockwise direction
                    #GPIO.output(Motor1B,GPIO.LOW) # put it high to rotate motor in anti-clockwise direction
                    #sleep(time)
                    #GPIO.output(Motor1A,GPIO.LOW)
                    #GPIO.output(Motor1B,GPIO.LOW)
                    
                    
        #text = font.render(latlong, True, green, blue)
        #display_surface.fill(white)
        #display_surface.blit(text, textRect)
        #pygame.display.update()
        page = wikipedia.page(query)
        wiki_text = wikipedia.summary(query, sentences=5)
        print (wiki_text)
        file1.write(wiki_text)
        file1.close() 
    url = page.url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')
    totalimages = min(len(images),35)
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
        language_code="en-IN",
        name="en-IN-Wavenet-C",
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
    pygame.mouse.set_visible(True)
    display_surface = pygame.display.set_mode((X, Y))
    os.system('feh -Y -x -q -D 2 -B black -F -Z -z --on-last-slide quit --caption-path /home/pi/Captions -r /home/pi/Images')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

                # deactivates the pygame library
                pygame.quit()

                # quit the program.
                quit()

            # Draws the surface object to the screen.
                pygame.display.update()
GPIO.cleanup()