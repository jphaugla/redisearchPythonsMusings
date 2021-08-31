import os
from redisearch import Client, TextField, NumericField, Query

client = Client('myIndex', '34.139.251.110', 15999)
print("connect successful")
# Creating the index definition and schema
# client.drop_index();
# client.create_index([TextField('title', weight=5.0), TextField('body'), TextField('phonetic')])
base_directory = "data/"
cnt = 0
for (dirpath, dirnames, filenames) in os.walk(base_directory):
    print("dirpath=" + dirpath)
    for file in filenames:
        print("file=" + file)
        if ("txt" in file):
            shortname = file.replace(".txt","")
            print("shortname is" + shortname)
            openname = dirpath + "/" + file
            print("openname is " + openname)
            f = open(openname)
            fileText = f.read()
            client.add_document(shortname, title=shortname, body=fileText, phoneticBody=fileText)

