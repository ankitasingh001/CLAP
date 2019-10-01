# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 18:47:23 2019

@author: chikki
"""
import glob
import re
import csv
import os
from operator import add
from pathlib import Path
from bs4 import BeautifulSoup
#import urllib2
import requests
from lxml import html

USERNAME = "speechtotextadmin"
PASSWORD = "speechtotext"

LOGIN_URL = "http://speechtotext.cse.iitb.ac.in/admin/login/"
URL = "http://speechtotext.cse.iitb.ac.in/admin/speechtotextbackend/uploadtextfile/add/"

def main():
    my_path = '/home/chikki/CLAPtest/text_files/Hindi'
    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]

    # Create payload
    payload = {
        "username": USERNAME, 
        "password": PASSWORD, 
        "csrfmiddlewaretoken": authenticity_token
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Scrape url
    result = session_requests.get(URL, headers = dict(referer = URL))
    soup = BeautifulSoup(session_requests.get(URL).content, 'lxml')
    print(soup.title)
    result = session_requests.get(URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]

    payload = {
        "csrfmiddlewaretoken": authenticity_token
    }
    for file in Path(my_path).glob('**/*.txt'):  
        files = {'TextFile': open(str(file), 'rb')}

        r = session_requests.post(URL,data = payload, files=files)
        #print(r.text)
#print(soup)
    

if __name__ == '__main__':
    main()