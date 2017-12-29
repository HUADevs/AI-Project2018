import os
import snowboydecoder
import signal
from bot import Bot

interrupted = False
assistant = Bot()
print('Starting assistant... Press Ctrl+C to exit')
# os.system('aplay -q /path/to/startup/.wav/file')

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


models = "/path/to/.pmdl/file"

def detected():
    detector.terminate()
    assistant.start()
    detector.start(detected_callback=callbacks,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)


callbacks = detected

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(models, sensitivity=0.5)
print('Listening...')

# main loop
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
