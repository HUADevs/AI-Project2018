#!/usr/bin/python3
import re

import requests
import os
import json
import traceback
import wikipedia
from speech import Speech
from knowledge import Knowledge
from phrases import Phrases
import time

wit_ai_token = "Bearer B5VCVURAJ3XPKVE3UUK7ENCNVDHNJCD3"
weather_api_token = "73995c4fbf4f6cd3fe31eb7ca4b3bdec"


class Bot(object):
    def __init__(self, trigger_word=None):
        self.phrases = Phrases()
        self.speech = Speech()
        self.knowledge = Knowledge()
        self.trigger_word = trigger_word

    def start(self):
        if self.trigger_word is not None:
            while 1:
                if self.is_called():
                    self.decide_action()
        else:
            self.decide_action()

    def is_called(self):
        speech = self.speech.listen_for_trigger_word()
        if speech is not None:
            if self.trigger_word.lower() in speech.lower():
                return True
        return False

    def decide_action(self):
        recognizer, audio = self.speech.listen_for_audio()

        # received audio data, now we'll recognize it using Google Speech Recognition
        speech = self.speech.google_speech_recognition(recognizer, audio)

        if speech is not None:
            try:
                r = requests.get('https://api.wit.ai/message?v=20160918&q=%s' % speech,
                                 headers={"Authorization": wit_ai_token})
                json_resp = json.loads(r.text)
                entities = None
                intent = None
                if 'entities' in json_resp and 'intent' in json_resp['entities']:
                    entities = json_resp['entities']
                    intent = json_resp['entities']['intent'][0]["value"]
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
                    print(json_resp)
                    self.__datetime_action(entities)
                elif intent == 'weather':
                    self.__weather_action()
                elif intent == 'search':
                    self.__search_action(entities)
                else:  # No recognized intent
                    print('Intent not recognized')
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
            self.speech.synthesize_text(text)

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




if __name__ == "__main__":
    bot = Bot(trigger_word='Siri')
    bot.start()
