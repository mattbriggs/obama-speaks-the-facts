'''Scratch file for getting Obama to say something.'''

import os
import requests

def get_obama(phrase="dog dog"):
    '''With a phrase return a URL for an MP4 of Obama saying it.'''

    outlink = "http://talkobamato.me/synthesize.py?speech_key="

    # prepare the phrase for the form post
    phrase = phrase.strip()
    phrase = phrase.replace(" ", "+")
    payload = "input_text=" + phrase

    #send the phrase and get the URL from the return
    response = requests.post("http://talkobamato.me/synthesize.py", payload)
    text = response.content.decode("utf-8")

    #get from the return if the reload already exists
    if text.find("reloadIfExists(") > 0:
        start_key = text.find("reloadIfExists(")
        end_key = start_key + 46
        keyid = text[start_key+15:end_key]

    #get from the return if the reload is being created
    elif text.find("obama.mp4") > 0:
        start_key = text.find("synth/output/")
        end_key = text.find("obama.mp4")
        keyid = text[start_key+13:end_key-1]
    else:
        keyid = "nokey"
    
    # create the URL
    myURL = outlink + keyid
    return myURL

print(get_obama("No one makes the cake like I do"))