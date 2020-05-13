# -*- coding: utf-8 -*-
import os
import filecmp
import glob
import re
import csv
from operator import add
from pathlib import Path

textdir = '/home/bhaskar/speechtotext/speechtotext/text_files/'
audiodir = '/home/bhaskar/speechtotext/speechtotext/text_audio_files/'


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
    countchar = 0 
    unwanted_symbols = ['/', '-', '[', '\\', ']', '॥', '।' ,'<', '>', '”', '“', '*', '*']
    if string == "":
        return False,countchar
    for symbol in unwanted_symbols:
        if string.find(symbol) != -1:
            return False,countchar
        if re.match(regex, string):
            return False,countchar		
        if re.match(regex2, string):
            return False,countchar
        if re.match(regex3, string):
            return False,countchar
        if string.find("/") != -1:
            return False,countchar
        if string.find('-') != -1:
            return False,countchar
        if string.find('[') != -1:
            return False,countchar
        if string.find("\\") != -1:
            return False,countchar
        if string.find(']') != -1:
            return False,countchar
        if string.find('॥') != -1:
            return False,countchar
        if string.find('।') != -1:
            return False,countchar
        if string.find('<') != -1:
            return False,countchar
        if string.find('>') != -1:
            return False,countchar
        if string.find('”') != -1:
            return False,countchar
        if string.find('“') != -1:
            return False,countchar
        for ch in range(0,26):
            if string.find(chr(65+ch)) != -1 or string.find(chr(97+ch)) != -1:
                countchar = 1
                return False,countchar
			
        return True,countchar

# Segreggating the text file into sentences
def make_textfile_object(sentences, min_length, max_length, task_type_dum, task_type, language, source, book_name):
    count_list = []
    filtered_sentences  = []
    filtered_sentences_specialchar = []
    filtered_sentences_length = []
    totalcount =0
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
        a,b = checks(dat)
        if len_dat >= min_length and len_dat <= max_length and a==True:
            filtered_sentences.append(dat)
        if len_dat >= min_length and len_dat <= max_length:
            filtered_sentences_length.append(dat)
        if a==True:
            filtered_sentences_specialchar.append(dat)
        if a==False:
            totalcount +=b

    count_list.append(len(filtered_sentences_specialchar))
    count_list.append(len(filtered_sentences_length))
    count_list.append(len(filtered_sentences))

    return count_list,totalcount

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




#def compare_dir_layout(dir1, dir2):
#    def _compare_dir_layout(dir1, dir2):
#        for (dirpath, dirnames, filenames) in os.walk(dir1):
#            for dirname in dirnames:
#                relative_path = dirpath.replace(dir1, "")
#                if os.path.exists( dir2 + relative_path ) == True:
#                    print (dir1+relative_path+"/"+dirname)
#                    list = os.listdir(dir1+relative_path+"/"+dirname+"/") # dir is your directory path
#                    print( len(list))
#        return
#
#    print ('files in "' + dir2 + '" but not in "' + dir1 +'"')
#    _compare_dir_layout(dir2, dir1)

match =0
regex = '[!|?|\.|\"|\'|\*|\-|\[|\]]'
regex_dot = r'[^\.!?]*[!\?\.]'
regex_quote = r'[\"][^\"]*[\"]'
regex_quote2 = r'[\'][^\']*[\']'
regex_colon = '[^\.!?:]*[:][^\.!?:]*'

f = open("Tasks.csv", "w+") 
for file in Path(textdir).glob('**/*.txt'):    
    taskvalue =[]
    textFile_str = str(file)
    path_list = textFile_str.split(os.sep)
    total = 0
    language = path_list[6]
    source   = path_list[7]
    print(language,source)
    min_length,max_length = update_length(language)
    #print(textFile_str)
    relpath = (os.path.dirname(os.path.abspath(textFile_str)))
    taskvalue.append(textFile_str)
    taskvalue.append(language)
    taskvalue.append(source)
    textFile = open(textFile_str, 'rb')	
    
    data = textFile.read()
    data = data.decode('utf-8')
    data = re.sub('[\n0-9()]', ' ', data)
    data = re.sub(' +', ' ',data)
    data = re.sub('\n+', '', data)
    textFile_str = textFile_str.split('/')[-1].split('.')[0]
    quote_data = re.findall(regex_quote, data)
    max_pk1,count  = make_textfile_object(quote_data, min_length, max_length, "quote", "Conversational", language,source, textFile_str)
    data = re.sub(regex_quote, '' ,data)
    total = total +count
    quote_data2 = re.findall(regex_quote2, data)
    len_quote = len(quote_data2+quote_data)
    max_pk2,count = make_textfile_object(quote_data2, min_length, max_length, "quote2","Conversational", language, source, textFile_str)
    #max_pk = list(map(add, max_pk1, max_pk2))
    total = total +count
    data = re.sub(regex_quote2, '' ,data)			
    diag_data = re.findall(regex_colon, data)
    max_pk,count = make_textfile_object(diag_data, min_length, max_length, "diag","Dialouge", language, source, textFile_str)
    total = total +count
    data = re.sub(regex_colon, '' ,data)
    
    # Defining split conditions 
    if language == 'Hindi':
        reg_data = data.split('।')
    else :
        reg_data = re.findall(regex_dot, data)
    max_pk,count = make_textfile_object(reg_data, min_length, max_length, "regular","Regular", language, source, textFile_str)
    total = total +count
    total_data = len(reg_data+diag_data+quote_data+quote_data2)
    taskvalue.append(total_data)
    exhaustedtasks = 0;
    relative_path = relpath.replace(textdir, "")
    if os.path.exists( audiodir + relative_path ) == True:
        print (audiodir+relative_path+"/")
        list = os.listdir(audiodir+relative_path+"/") # dir is your directory path
        exhaustedtasks = int(len(list)/3)
    print(exhaustedtasks)
    taskvalue.append(exhaustedtasks)
    
    write_list_to_file(taskvalue,f.name)

#compare_dir_layout(textdir, audiodir)
