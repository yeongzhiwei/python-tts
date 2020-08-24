import logging
from queue import Queue
from threading import Thread

import azure.cognitiveservices.speech as speechsdk

try:
    from config import config
    subscription = config['speech_key']
    region = config.get('service_region', 'southeastasia')
    voice = config.get('voice_name', 'en-US-GuyNeural')
    log_file = config.get('log_file_name', 'tts.log')
except ImportError:
    print("Missing config.py file")
    import sys
    sys.exit(1)

logging.basicConfig(
    format='%(asctime)-15s: %(levelname)-8s %(message)s',
    filename=log_file, 
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info('Started Text to Speech CLI')
print(">>> Starting text-to-speech service enabled by Azure Cognitive Services")
print(">>> Enter the text you want to speak or enter quit to terminate")

speech_config = speechsdk.SpeechConfig(subscription=subscription, region=region)
speech_config.speech_synthesis_voice_name = voice
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

speech_synthesizer.synthesis_started.connect(lambda evt: logging.info(f'{evt.result.result_id}: Started'))
speech_synthesizer.synthesis_completed.connect(lambda evt: logging.info(f'{evt.result.result_id}: Completed'))
speech_synthesizer.synthesis_canceled.connect(lambda evt: logging.info(f'{evt.result.result_id}: Cancelled'))
speech_synthesizer.synthesis_canceled.connect(lambda evt: logging.info(f'Error: {evt.result.cancellation_details}'))

texts = Queue()
hasError = False

def speak():
    global hasError
    while (True):
        text = texts.get()
        if text == 'quit':
            break
        logging.info(f'Synthesizing "{text}"')
        result = speech_synthesizer.speak_text(text)
        if result.reason == speechsdk.ResultReason.Canceled:
            hasError = True
            break
        logging.info(f'{result.result_id}: "{text}"')

thread = Thread(target=speak)
thread.start()

while (True):
    print('>', end=' ')
    text = input()
    if hasError:
        print(">>> An error occurred. Check the logs.")
        break
    if len(text.strip()) > 0:
        texts.put(text)
    if text == 'quit':
        break

thread.join()
print(">>> Stopped text-to-speech service")
logging.info('Stopped Text to Speech CLI')