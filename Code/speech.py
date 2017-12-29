#!/usr/bin/python
import os
import speech_recognition as sr
from gtts import gTTS


class Speech(object):

    def google_speech_recognition(self, recognizer, audio, language="el-GR"):
        speech = None
        try:
            speech = recognizer.recognize_google(audio_data=audio, language=language)
            print("Request: {sentence}".format(sentence=speech))
        except sr.UnknownValueError:
            print("Could not understand audio")
            self.synthesize_text('Δεν το\'πιασα. Πες το άλλη μία')
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        return speech

    def listen_for_audio(self):
        # obtain audio from the microphone
        r = sr.Recognizer()
        m = sr.Microphone()

        with m as source:
            r.adjust_for_ambient_noise(source)
            print("I'm listening...")
            os.system('aplay -q /home/didymos/Documents/AI_Project/audio_files/triggered.wav')
            audio = r.listen(source)

        print("Found audio")
        return r, audio

    def listen_for_trigger_word(self, language="el-GR"):
        # obtain audio from the microphone
        r = sr.Recognizer()
        m = sr.Microphone()

        with m as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        speech = None
        try:
            speech = r.recognize_google(audio_data=audio, language=language)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        return speech

    def synthesize_text(self, text):
        tts = gTTS(text=text, lang='el', slow=False)
        tts.save("/home/didymos/Documents/AI_Project/audio_files/tmp.mp3")

        print('Response: {response}'.format(response=text))
        os.system("mpg123 -q /home/didymos/Documents/AI_Project/audio_files/tmp.mp3")
        os.remove("/home/didymos/Documents/AI_Project/audio_files/tmp.mp3")
