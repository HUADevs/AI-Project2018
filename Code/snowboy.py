import os
import signal
import snowboydecoder
from bot import Bot

interrupted = False
assistant = Bot(speech_input=True)
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
print('Starting assistant... Press Ctrl+C to exit')
os.system('aplay -q {dir}/audio_files/startup.wav'.format(dir=DIRECTORY))

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


models = '{dir}/resources/alexa.umdl'.format(dir=DIRECTORY)


def detected():
    detector.terminate()
    assistant.start()
    detector.start(detected_callback=callbacks,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

callbacks = detected

detector = snowboydecoder.HotwordDetector(models, sensitivity=0.5)


def main():
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    print('Listening...')

    # main loop
    detector.start(detected_callback=callbacks,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

    detector.terminate()


if __name__ == '__main__':
    main()
