import os
import redis

redis_password = ""
if os.environ.get('REDIS_SERVER') is not None:
    redis_server = os.environ.get('REDIS_SERVER')
    print("passed in redis server is " + redis_server)
else:
    redis_server = 'redis'
    print("no passed in redis server variable ")

if os.environ.get('REDIS_PORT') is not None:
    redis_port = int(os.environ.get('REDIS_PORT'))
    print("passed in redis port is " + str(redis_port))
else:
    redis_port = 6379
    print("no passed in redis port variable ")
if os.environ.get('REDIS_PASSWORD') is not None:
    redis_password = os.environ.get('REDIS_PASSWORD')
    print("passed in redis password is " + redis_password)

if redis_password is not None:
    conn = redis.StrictRedis(redis_server, redis_port, password=redis_password,
                             decode_responses=True)
else:
    conn = redis.StrictRedis(redis_server, redis_port, decode_responses=True)
print("connect successful")

base_directory = "/home/jovyan/fileload/data/"
cnt = 0
for (dirpath, dirnames, filenames) in os.walk(base_directory):
    print("dirpath=" + dirpath)
    for file in filenames:
        print("file=" + file)
        if ("txt" in file):
            shortname = file.replace(".txt", "")
            print("shortname is" + shortname)
            openname = dirpath + "/" + file
            print("openname is " + openname)
            f = open(openname)
            fileText = f.read()
            conn.hset("file:" + shortname, "body", fileText)
            conn.hset("file:" + shortname, "phoneticBody", fileText)
