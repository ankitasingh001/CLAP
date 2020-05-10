import psycopg2
import datetime
import csv
import numpy as np

try:
   connection = psycopg2.connect(user="speechtotext",
                                  password="speechtotext",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="speechtotextdb")
   cursor = connection.cursor()
   file = open("audio.txt", "w")
   AUDIO_QUALITY = ['Audio is fine', 'Noisy', 'Not Audible', 'Robotic/Artificial','Incomplete audio','Text and audio do not match','Speaker unclear']
   audio_quality = "select count(*),audio_quality from speechtotextbackend_textfileappuserverify where \"verificationDateTime\">='2019-08-30'  and \"verificationDateTime\"< CURRENT_TIMESTAMP group by audio_quality"
   audio_data = "select count(*),audio_quality from speechtotextbackend_textfileappuserverify where \"verificationDateTime\">='2019-08-30'  and \"verificationDateTime\"< CURRENT_TIMESTAMP and audio_quality like '%"+AUDIO_QUALITY[0]+"%'group by audio_quality"
   mismatch = " select  count(*) from speechtotextbackend_textfileappuser where \"conversionDateTime\">='2019-08-30'  and \"conversionDateTime\"< CURRENT_TIMESTAMP and verifications = 3"
   total_verifies = "select sum(verifications) from speechtotextbackend_textfileappuser where \"conversionDateTime\">='2019-08-30'  and \"conversionDateTime\"< CURRENT_TIMESTAMP "
   
   for text in AUDIO_QUALITY:
       audio_data = "select count(*) from speechtotextbackend_textfileappuserverify where \"verificationDateTime\">='2019-08-30'  and \"verificationDateTime\"< CURRENT_TIMESTAMP and audio_quality like '%"+text+"%'"
       
       cursor.execute(audio_data)
       records = cursor.fetchall() 
       for row in records:
           print(text," ", str(row[0]))
           file.write(text+" "+str(row[0])+"\n")
   fulldata = np.array([])
   for text in AUDIO_QUALITY:
       audio_data = " Select count(*),speechtotextbackend_textfile.language from speechtotextbackend_textfileappuserverify,speechtotextbackend_textfileappuser,speechtotextbackend_textfile where speechtotextbackend_textfileappuserverify.\"textFileAppUser_id\" = speechtotextbackend_textfileappuser.id and speechtotextbackend_textfileappuser.\"textFile_id\" = speechtotextbackend_textfile.id  and speechtotextbackend_textfileappuserverify.\"verificationDateTime\">='2019-08-30'  and speechtotextbackend_textfileappuserverify.\"verificationDateTime\"< CURRENT_TIMESTAMP and speechtotextbackend_textfileappuserverify.audio_quality like '%"+text+"%' group by speechtotextbackend_textfile.language"  
       cursor.execute(audio_data)
       records = cursor.fetchall()
       fulldata= np.append(fulldata,(np.array(records)))
       for row in records:
           print(" ", str(row[0])," ",str(row[1])+ " "+text)
           file.write(" "+ str(row[0])+" "+str(row[1])+ " "+text+"\n")
       file.write("\n")
   #print(fulldata)
       

#   with open("audiocomments.csv", 'w') as file:
#       writer = csv.writer(file)
#       writer.writerow(AUDIO_QUALITY)
#            
#       for row in ((np.squeeze(np.array(fulldata))).T):
#               #print(" ", str(row[0])," ",str(row[1])+ " "+text)
#           writer.writerow(row)
       #file.write(text+" "+str(row[0])+"\n")
           
   #audio_data = " Select count(*),speechtotextbackend_textfile.language,speechtotextbackend_textfileappuserverify.audio_quality from speechtotextbackend_textfileappuserverify,speechtotextbackend_textfileappuser,speechtotextbackend_textfile where speechtotextbackend_textfileappuserverify.\"textFileAppUser_id\" = speechtotextbackend_textfileappuser.id and speechtotextbackend_textfileappuser.\"textFile_id\" = speechtotextbackend_textfile.id  and speechtotextbackend_textfileappuserverify.\"verificationDateTime\">='2019-08-30'  and speechtotextbackend_textfileappuserverify.\"verificationDateTime\"< CURRENT_TIMESTAMP and speechtotextbackend_textfileappuserverify.audio_quality like '%"+text+"%' group by speechtotextbackend_textfile.language,speechtotextbackend_textfileappuserverify.audio_quality"  
   cursor.execute(total_verifies)
   records = cursor.fetchall() 
   print("count of total verifications done :", records[0][0] )
   file.write("count of total verifications done :"+str( records[0][0])+"\n")
   
   cursor.execute(mismatch)
   records = cursor.fetchall() 
   print("count of mismatched verifies", records[0][0] )
   file.write("count of mismatched verifies "+str( records[0][0])+"\n")
   
   file.close()    
except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")