import os
from redisearch import Client, TextField, NumericField, Query

if os.environ.get('REDIS_SERVER') is not None:
    redis_server = os.environ.get('REDIS_SERVER')
else:
    redis_server = 'redis'

if os.environ.get('REDIS_PORT') is not None:
    redis_port = int(environ.os.get('REDIS_PORT'))
else:
    redis_port = 6379

client = Client('myIndex', redis_server, redis_port)
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

