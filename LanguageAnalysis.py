# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 10:20:34 2019

@author: Ankita Singh
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 15:55:04 2019

@author: Ankita Singh
"""

import glob
import re
import csv
import os
from operator import add
from pathlib import Path

#Defining minimum/ maximum lengths for all languages

MIN_MAR = 4
MAX_MAR = 14

MIN_TAM = 3
MAX_TAM = 12

MIN_MAL = 3
MAX_MAL = 12

#Divide two numbers 
def div(x,y):
    try:
        return x/y
    except ZeroDivisionError:
        return 0
        
# generate csv file from observed data
def write_list_to_file(guest_list, filename):
    with open(filename,'a') as outfile:
        wr = csv.writer(outfile, dialect='excel')
        wr.writerow(guest_list)

# Performing the filteration of sentences/tasks
def checks(string):
    regex = '-'
    regex1 = '[A-Za-z]+'
    regex2 = '/'
    regex3 = '\/'
		
    unwanted_symbols = ['/', '-', '[', '\\', ']', '॥', '।' ,'<', '>', '”', '“', '*', '*']
    if string == "":
        return False
    for symbol in unwanted_symbols:
        if string.find(symbol) != -1:
            return False
        if re.match(regex, string):
            return False		
        if re.match(regex2, string):
            return False
        if re.match(regex3, string):
            return False
        if string.find("/") != -1:
            return False
        if string.find('-') != -1:
            return False
        if string.find('[') != -1:
            return False
        if string.find("\\") != -1:
            return False
        if string.find(']') != -1:
            return False
        if string.find('॥') != -1:
            return False
        if string.find('।') != -1:
            return False
        if string.find('<') != -1:
            return False
        if string.find('>') != -1:
            return False
        if string.find('”') != -1:
            return False
        if string.find('“') != -1:
            return False
        for ch in range(0,26):
            if string.find(chr(65+ch)) != -1 or string.find(chr(97+ch)) != -1:
                return False
			
        return True

# Segreggating the text file into sentences
def make_textfile_object(sentences, min_length, max_length, task_type_dum, task_type, language, source, book_name):
    count_list = []
    filtered_sentences  = []
    filtered_sentences_specialchar = []
    filtered_sentences_length = []
    for dat in sentences:
        dat = dat.replace('\xc2\xa0', '')
        dat = dat.replace('\n', '')
        dat = dat.replace('  ', '')
        dat = dat.strip()
        if task_type_dum == 'quote':
             dat = dat.split('"')[1]
             dat = dat.strip()
        elif task_type_dum == 'quote2':
             dat = dat.split("'")[1]
             dat = dat.strip()
        elif task_type_dum == 'diag':
            dat = dat.split(':')[-1]
            dat = dat.strip()
        len_dat = len(dat.split(' '))
        if len_dat >= min_length and len_dat <= max_length and checks(dat)==True:
            filtered_sentences.append(dat)
        if len_dat >= min_length and len_dat <= max_length:
            filtered_sentences_length.append(dat)
        if checks(dat)==True:
            filtered_sentences_specialchar.append(dat)

    count_list.append(len(filtered_sentences_specialchar))
    count_list.append(len(filtered_sentences_length))
    count_list.append(len(filtered_sentences))

    return count_list

#Updating lengths for different languages used    
def update_length(language):
    if language == 'Tamil':
        min_length = MIN_TAM
        max_length = MAX_TAM
    elif language == 'Marathi' or language=='Telugu' or language=='Hindi':
        min_length = MIN_MAR
        max_length = MAX_MAR
    elif language == "Malayalam":
        min_length = MIN_MAL
        max_length = MAX_MAL
    return min_length,max_length

#Code for calculating wastage and writing it into csvfile
match =0
my_path = '/home/chikki/text_files/'
regex = '[!|?|\.|\"|\'|\*|\-|\[|\]]'
regex_dot = r'[^\.!?]*[!\?\.]'
regex_quote = r'[\"][^\"]*[\"]'
regex_quote2 = r'[\'][^\']*[\']'
regex_colon = '[^\.!?:]*[:][^\.!?:]*'

f = open("info.csv", "w+") 

for file in Path(my_path).glob('**/*.txt'):    
    taskvalue =[]
    textFile_str = str(file)
    path_list = textFile_str.split(os.sep)
    
    language = path_list[4]
    source   = path_list[5]
    min_length,max_length = update_length(language)
    print(textFile_str)
    taskvalue.append(textFile_str)
    taskvalue.append(language)
    taskvalue.append(source)
    textFile = open(textFile_str, 'rb')	
    
    data = textFile.read()
    data = data.decode('utf-8')
    data = re.sub('[\n0-9()]', ' ', data)
    data = re.sub(' +', ' ',data)
    data = re.sub('\n+', '', data)
    
    # Finding quotationd and wasted quotations in the files
    textFile_str = textFile_str.split('/')[-1].split('.')[0]
    quote_data = re.findall(regex_quote, data)
    max_pk1  = make_textfile_object(quote_data, min_length, max_length, "quote", "Conversational", language,source, textFile_str)
    data = re.sub(regex_quote, '' ,data)
    
    quote_data2 = re.findall(regex_quote2, data)
    len_quote = len(quote_data2+quote_data)
    taskvalue.append(len_quote)
    max_pk2 = make_textfile_object(quote_data2, min_length, max_length, "quote2","Conversational", language, source, textFile_str)
    max_pk = list(map(add, max_pk1, max_pk2))
    
    waste_quote = (len_quote - max_pk[2])
    waste_quotepercent= div((len_quote - max_pk[2])*100,len_quote)
    #Finding dialogues and wasted dialogues
    
    taskvalue.append(max_pk)
    data = re.sub(regex_quote2, '' ,data)			
    diag_data = re.findall(regex_colon, data)

    taskvalue.append(len(diag_data))
    max_pk = make_textfile_object(diag_data, min_length, max_length, "diag","Dialouge", language, source, textFile_str)
    waste_diag = len(diag_data) - max_pk[2]
    waste_diagpercent= div((len(diag_data) - max_pk[2])*100,len(diag_data))
    taskvalue.append(max_pk)
    data = re.sub(regex_colon, '' ,data)
    
    # Defining split conditions 
    if language == 'Hindi':
        reg_data = data.split('।')
    else :
        reg_data = re.findall(regex_dot, data)
    #Finding wastage of regular sentences
    taskvalue.append(len(reg_data))
    max_pk = make_textfile_object(reg_data, min_length, max_length, "regular","Regular", language, source, textFile_str)
    taskvalue.append(max_pk)
    
    waste_reg = len(reg_data) - max_pk[2]
    waste_regpercent= div((len(reg_data) - max_pk[2])*100,len(reg_data))
    total_data = len(reg_data+diag_data+quote_data+quote_data2)
    
    taskvalue.append(round(waste_quotepercent,2))
    taskvalue.append(round(waste_diagpercent,2))
    taskvalue.append(round(waste_regpercent,2))
    
    #Total wastage percentage    
    totalwaste_percent = div(((waste_diag + waste_quote + waste_reg)*100.0),total_data)
    taskvalue.append(round(totalwaste_percent,2))
    # Writing each row to file
    write_list_to_file(taskvalue,f.name)
    
