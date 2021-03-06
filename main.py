'''Matt Briggs homework assignment.'''

import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_fact():
    '''Retreive a fact from unkno. '''
    response = requests.get("http://unkno.com")
    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()

def get_obama(phrase="Thanks Obama"):
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

@app.route('/')
def home():
    '''Return the URL that points to Mr. Obama saying a fact.'''
    fact = get_fact()
    factURL = get_obama(fact)
    page = '''<h1>Mr. Obama has the facts.</h1>
    <p>When you click on the following link, a URL will take you to the 
    recording of the former president saying a random fact. Random, but a
    fact.</p>
    <p><a href="{}">Thanks Obama!</a></p>'''.format(factURL)

    return page

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='localhost', port=port)