'''Scratch file for getting a fact.'''

import os

import requests
from bs4 import BeautifulSoup

def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    string = facts[0].getText()
    string = string.strip()
    return string

print(get_fact())