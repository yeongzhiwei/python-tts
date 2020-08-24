# Text-to-Speech CLI

A Python script to start text to speech CLI enabled by Azure Cognitive Services.

## Pre-requisite

- Require subscription to Azure Cognitive Services
- Set `speech_key` in `config.py` to the API key of Azure Cognitive Services

## Usage

```bash
    $ cd /to/this/path
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install azure-cognitiveservices-speech
    (venv) $ python3 main.py
    >>> Starting text-to-speech service enabled by Azure Cognitive Services
    >>> Enter the text you want to speak or enter quit to terminate
    > Hello world
    > ...
    > quit
    >>> Stopped text-to-speech service
```

## Use case

As a deaf person, I did not learn how to speak while growing up. I found it useful to voice what I typed so that everyone in the room can hear instead of having them read the text off the screen. Working with people over the years, I found that it's easier for people to hear than to read and had I just typed, someone would invariably pronounce the text.

## Technical notes

I tested this using Python 3.7.3 on macOS.
