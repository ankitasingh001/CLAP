import psycopg2
import datetime

try:
   connection = psycopg2.connect(user="speechtotext",
                                  password="speechtotext",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="speechtotextdb")
   cursor = connection.cursor()
   file = open("queries_back.txt", "a+")
   Users_joined = "select count(*) from speechtotextbackend_user where created >='2020-02-15' and created < CURRENT_TIMESTAMP"
   audiolen_hindi = "select sum(\"audio_length\") from speechtotextbackend_textfileappuser where \"conversionDateTime\">='2020-02-15'  and \"conversionDateTime\"< CURRENT_TIMESTAMP and \"audioFile\" like 'text_audio_files/Hindi/%'"
   audiolen_marathi = "select sum(\"audio_length\") from speechtotextbackend_textfileappuser where \"conversionDateTime\">='2020-02-15'  and \"conversionDateTime\"< CURRENT_TIMESTAMP and \"audioFile\" like 'text_audio_files/Marathi/%'"
   audiolen_tamil = "select sum(\"audio_length\") from speechtotextbackend_textfileappuser where \"conversionDateTime\">='2020-02-15'  and \"conversionDateTime\"< CURRENT_TIMESTAMP and \"audioFile\" like 'text_audio_files/Tamil/%'"
   audiolen_telugu = "select sum(\"audio_length\") from speechtotextbackend_textfileappuser where \"conversionDateTime\">='2020-02-15'  and \"conversionDateTime\"< CURRENT_TIMESTAMP and \"audioFile\" like 'text_audio_files/Telugu/%'"
   audiolen_total =  "select sum(\"audio_length\") from speechtotextbackend_textfileappuser where \"conversionDateTime\">='2020-02-15'  and \"conversionDateTime\"< CURRENT_TIMESTAMP "
   audio_quality = "select count(*),audio_quality from speechtotextbackend_textfileappuserverify where \"verificationDateTime\">='2020-02-15'  and \"verificationDateTime\"< CURRENT_TIMESTAMP group by audio_quality"
   tasks_per_language = "select count(*),language from speechtotextbackend_textfileappuser,speechtotextbackend_textfile where speechtotextbackend_textfile.id = speechtotextbackend_textfileappuser.\"textFile_id\" and speechtotextbackend_textfileappuser.\"conversionStatus\"=2 and speechtotextbackend_textfileappuser.\"conversionDateTime\">='2020-02-15'  and speechtotextbackend_textfileappuser.\"conversionDateTime\"< CURRENT_TIMESTAMP group by speechtotextbackend_textfile.language "
   
   cursor.execute(Users_joined)
   records = cursor.fetchall() 
   print("count of total users ", records[0][0] )
   file.write("count of total users joined after announcement: "+str( records[0][0])+"\n")
   
   cursor.execute(audiolen_hindi)
   records = cursor.fetchall() 
   print("count of total audio length in hindi ", records[0][0] )
   file.write("count of total audio length in hindi "+str( records[0][0])+"\n")
   
   cursor.execute(audiolen_marathi)
   records = cursor.fetchall() 
   print("count of total audio length in marathi", records[0][0] )
   file.write("count of total audio length in marathi "+str( records[0][0])+"\n")
   
   cursor.execute(audiolen_tamil)
   records = cursor.fetchall() 
   print("count of total audio length in tamil", records[0][0] )
   file.write("count of total audio length in tamil "+str( records[0][0])+"\n")
   
   cursor.execute(audiolen_telugu)
   records = cursor.fetchall() 
   print("count of total audio length in telugu", records[0][0] )
   file.write("count of total audio length in telugu "+str( records[0][0])+"\n")
   
   cursor.execute(audiolen_total)
   records = cursor.fetchall() 
   print("count of total audio length in total", records[0][0] )
   file.write("count of total audio length in total "+str( records[0][0])+"\n")
   
   cursor.execute(audio_quality)
   records = cursor.fetchall() 
   for row in records:
       print("audio quality", str(row[0])," ",str(row[1]) )
   #file.write("count of total audio length in total "+str( records[0][0])+"\n")
   cursor.execute(tasks_per_language)
   records = cursor.fetchall() 
   for row in records:
       print("Tasks completed for language", str(row[1])," = ",str(row[0]) )
   
   file.close()    
except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")