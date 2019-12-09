# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 09:45:21 2019

@author: Ankita Singh
"""

"""
To run this script periodically (for example every minute)
Type 'crontab -e' on linux terminal
Edit the file and add th follwoing : 
* * * * * python3 /home/chikki/CLAPtest/SendEmail.py

The second part is the location of the SendEmail.py file

Save and exit

"""

import smtplib
import urllib
import os


fromaddr = 'ankitasingh950910@gmail.com'  
toaddrs  = 'ankitasingh950910@gmail.com'  
msg = 'CLAP server is down'  

username = 'ankitasingh950910'  
password = 'QNMQ7S85'

#Send email via gmail smtp
def sendEmail():
    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(username, password)
        smtpserver.sendmail(fromaddr, toaddrs, msg)
        smtpserver.quit()
        print("Email sent successfully !")
    except Exception as e:
        print(e)
        
# Ping the server and see if it is up
def check_connection(url):
	response = os.system("ping -c 1 " + url)
	if response == 0:
		return True
	else:
		return False
  

url = "10.129.1.153" #Server where clap is running
#Sends email in case the server is down
if(check_connection(url)):
    sendEmail()
