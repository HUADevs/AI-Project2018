#!/usr/bin/python3
import re

import requests
import os
import json
import traceback
import wikipedia
from wit import Wit
from speech import Speech
from knowledge import Knowledge
from phrases import Phrases
from fatsecret import Fatsecret
from translate import Translator
import time

weather_api_token = "73995c4fbf4f6cd3fe31eb7ca4b3bdec"
fat_secret_oauth = "90fe184a283449ed8a83e35790c04d65"


class Bot(object):
    def __init__(self, trigger_word=None, speech_input=None):
        self.phrases = Phrases()
        self.speech = Speech()
        self.knowledge = Knowledge()
        self.trigger_word = trigger_word
        self.speech_input = speech_input
        self.witai = Wit("S73IKQDWJ22OJMOSD6AOT4CSJOWXIPX6")
        self.fs = Fatsecret("90fe184a283449ed8a83e35790c04d65", "054e80b2be154337af191be2c9e11c28")
        self.gr_to_en = Translator(from_lang="el",to_lang="en")
        self.en_to_gr = Translator(from_lang="en",to_lang="el")

    def start(self):
        if self.trigger_word and self.speech_input is not None:
            while 1:
                if self.is_called():
                    self.decide_action()
        else:
            print("Γεία σου! Πως θα μπορούσα να σε βοηθήσω;")
            while 1:
                self.decide_action()

    def is_called(self):
        speech = self.speech.listen_for_trigger_word()
        if speech is not None:
            if self.trigger_word.lower() in speech.lower():
                return True
        return False

    def decide_action(self):

        if self.speech_input is not None:
            recognizer, audio = self.speech.listen_for_audio()

        # received audio data, now we'll recognize it using Google Speech Recognition
            bot_input = self.speech.google_speech_recognition(recognizer, audio)
        else:
            bot_input = input()

        if bot_input is not None:
            try:
                resp = self.witai.message(bot_input)
                entities = None
                intent = None
                if 'entities' in resp and 'intent' in resp['entities']:
                    entities = resp['entities']
                    intent = resp['entities']['intent'][0]["value"]
                    print('Intent: {intent}'.format(intent=intent))
                if intent == 'greeting':
                    self.__text_action(self.phrases.greet())
                elif intent == 'tutorial':
                    self.__tutorial_action()
                elif intent == 'personal_status':
                    self.__personal_status()
                elif intent == 'beatbox':
                    self.__beatbox_action()
                elif intent == 'joke':
                    self.__joke_action()
                elif intent == 'datetime':
                    #print(resp)
                    self.__datetime_action(entities)
                elif intent == 'weather':
                    self.__weather_action()
                elif intent == 'search':
                    self.__search_action(entities)
                elif intent == 'food_det':
                    self.__food_action(entities)
                else:  # No recognized intent
                    #print('Intent not recognized')
                    self.__text_action(self.phrases.unrecognized_intent())
                    return

            except Exception as e:
                print("Exception occured")
                print(e)
                traceback.print_exc()
                self.__text_action("Έγινε κάποιο λάθος")
                return

    def __text_action(self, text=None):
        if text is not None:
            if self.speech_input is not None:
                self.speech.synthesize_text(text)
            else:
                print(text)

    def __tutorial_action(self):
        self.__text_action(self.phrases.tutorial())

    def __personal_status(self):
        self.__text_action(self.phrases.personal_status())

    def __beatbox_action(self):
        self.__text_action(self.phrases.beatbox())

    def __joke_action(self):
        joke = self.phrases.joke()
        for j in joke:
            time.sleep(1)
            self.__text_action(j)

    def __datetime_action(self, entities):
        dt = None
        if 'datetime' in entities:
            dt = entities['datetime'][0]['grain']
            print('Datetime: {dt}'.format(dt=dt))
        if str(dt) == 'second':
            self.__text_action('Η ώρα είναι {time}'.format(time=self.knowledge.get_time()))
        elif str(dt) == 'day':
            self.__text_action('Σήμερα είναι {weekday}'.format(weekday=self.knowledge.get_weekday()))
        elif str(dt) == 'ημερομηνία':
            self.__text_action('Σήμερα είναι {date}'.format(date=self.knowledge.get_date()))

    def __weather_action(self):
        weather_obj = self.knowledge.find_weather()
        self.__text_action('Η θερμοκρασία είναι ' + str(weather_obj['temperature']) + '° Κελσίου.')

    def __search_action(self, entities=None):
        self.__text_action(self.phrases.searching())
        if 'wikipedia_search_query' in entities:
            query = entities['wikipedia_search_query'][0]['value']
            print('wikipedia query: {query}'.format(query=query))
            wikipedia.set_lang("el")
            try:
                self.__text_action(re.sub(r'\([^)]*\)', '', wikipedia.summary(query, sentences=1)))
            except wikipedia.PageError as e:
                print(e)
                self.__text_action('Δεν βρήκα κάποιο αποτέλεσμα')
        else:
            self.__text_action('Δεν μου είπες τί να ψάξω')

    def __food_action(self,entities):
        self.__text_action(self.phrases.searching())
        inp=self.gr_to_en.translate(entities['food'][0]['value'])
        try:
            resp = self.fs.foods_search(inp)
            print(self.en_to_gr.translate(resp[0]["food_name"]) + "\n" + resp[0]["food_description"])
        except Exception as e:
            entities['wikipedia_search_query'][0]['value'] = entities['food'][0]['value']
            self.__search_action()

if __name__ == "__main__":
    bot = Bot(trigger_word='Siri')
    bot.start()
