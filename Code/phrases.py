import random
import datetime
import yaml


class Phrases(object):
    def __init__(self):
        # make random more random by seeding with time
        random.seed(datetime.datetime.now())

    @staticmethod
    def add_phrases(file, phrases):
        stream = open('yaml/' + file + '.yaml', 'a')
        yaml.safe_dump(phrases, stream)

    @staticmethod
    def get_phrases(file):
        stream = open('yaml/' + file + '.yaml', 'r')
        results = yaml.load(stream)
        if file == 'greetings_phrases.yaml':
            date = datetime.datetime.now()
            if date.hour < 6 or date.hour > 21:
                results = random.choice(["Καλό βράδυ", random.choice(results)])
            elif 6 < date.hour < 12:
                results = random.choice(["Καλημέρα", random.choice(results)])
            elif 12 <= date.hour <= 21:
                results = random.choice(["Καλησπέρα", random.choice(results)])

        return results

# def searching(self):
#     searching_phrases = [
#         "Άσε με να το ψάξω",
#         "Δώσ'μου δύο λεπτά",
#         "Μισό να το ψάξω"
#     ]
#     stream = open('search_phrases.yaml', 'w')
#     yaml.dump(searching_phrases, stream)
#     stream1 = open('search_phrases.yaml', 'r')
#     result = yaml.load(stream1)
#     print(result)
#
#     return random.choice(result)

# def personal_status(self, status_type=None):
#     positive_status = [
#         "Μια χαρά!",
#         "Μια χαρά! Εσύ;",
#         "Πολύ καλά! Ευχαριστώ"
#     ]
#
#     negative_status = []
#
#     moderate_status = []
#
#     if status_type == 'negative':
#         return random.choice(negative_status)
#     elif status_type == 'moderate':
#         return random.choice(moderate_status)
#
#     return random.choice(positive_status)
# #
# def joke(self):
#     jokes = [
#         ["Όταν ο παππούς μου ήταν νέος, η νεκρά θάλασσα ήταν ακόμα άρρωστη."],
#     ]
#
#     return random.choice(jokes)

# def greet(self):
#
#     greeting_words = [
#         "Γεια",
#         "Γεια χαρά"
#     ]
#
#     goofy_greetings = [
#         "Τί χαμπάρια;",
#         "Πώς πάει;",
#         "Τί νέα;"
#     ]
#
#     choice = random.randint(0, 4)
#     ret_phrase = ""
#
#     if (choice == 0) or (choice == 3):  # time related
#         ret_phrase = "%s" % self.time_of_day(datetime.datetime.now())
#     elif (choice == 1) or (choice == 4):  # standard greeting
#         ret_phrase = random.choice(greeting_words)
#     elif choice == 2:  # goofy greeting
#         ret_phrase = random.choice(goofy_greetings)
#
#     return ret_phrase

# def time_of_day(self, date):
#     ret_phrase = ""
#     if date.hour < 6 or date.hour > 21:
#         ret_phrase = "Καλό βράδυ"
#     elif 6 < date.hour < 12:
#         ret_phrase = "Καλημέρα"
#     elif 12 <= date.hour <= 21:
#         ret_phrase = "Καλησπέρα"
#
#     return ret_phrase

# def job_done(self):
#     phrases = [
#         "Κανένα πρόβλημα",
#         "Όπως θες",
#         "Φυσικά",
#         "Έγινε",
#         "Αποστολή εξετελέσθη",
#         "Όπως διατάξεις"
#     ]
#
#     return random.choice(phrases)

# def beatbox(self):
#     beats = [
#         'Τί λες γι\'αυτό. μπουτς εντ κατς εντ μπουτς εντ κατς εντ μπουτς εντ κατς εντ μπουτς. '
#         'Έχω και συνέχεια. κατς εν μπουτς εν κατς εν μπουτς εν κατς εν μπουτς'
#     ]
#
#     return random.choice(beats)
#
# def unrecognized_intent(self):
#     phrases = [
#         'Όπα. Δεν ξέρω τί να κάνω',
#         'Δεν έχω εκπαιδευτεί σε αυτό',
#         'Δεν ξέρω τί να κάνω ακόμα'
#     ]
#
#     return random.choice(phrases)
#
# def tutorial(self):
#     phrases = [
#         'Ξέρω beatbox',
#         'Μπορώ να σου πω ανέκδοτο',
#         'Μπορώ να σου πώ την ώρα, την μέρα ή την ημερομηνία',
#         'Μπορώ να σου πω τον καιρό για σήμερα',
#         'Μπορώ να ψάξω στην βικιπέδια'
#     ]
#
#     return random.choice(phrases)
