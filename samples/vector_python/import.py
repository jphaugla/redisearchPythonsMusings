import csv
import os
import json
import redis
from redis.commands.search.field import (
    TextField,
    TagField,
    NumericField,
    VectorField
)
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
import numpy as np
from sentence_transformers import SentenceTransformer


# Constants
CREATE_IDX = True

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

if os.environ.get('VECTOR_DATA_PATH') is not None:
    data_path = os.environ.get('VECTOR_DATA_PATH')
    print("passed in data path is " + data_path)
else:
    data_path = "/home/jovyan/vector_python/"
    print("no passed in redis port variable ")

if redis_password is not None:
    conn = redis.Redis(redis_server, redis_port, password=redis_password)
else:
    conn = redis.Redis(redis_server, redis_port)
print("connect successful")

# flush the database
conn.flushdb()
# Opens a JSON file
f = open(data_path + "bikes.json")

# Loads JSON objects as dictionaries
data = json.load(f)

# Load the machine learning model
model = SentenceTransformer('sentence-transformers/all-distilroberta-v1')

print("start data insert")
# Insert the data
i = 0
p = conn.pipeline(transaction=False)
for bike in data:
    keyname = "bike:{}".format(i)
    del bike["specs"]
    bike["description_embeddings"] = model.encode(bike["description"]).astype(np.float32).tobytes()
    p.hset(keyname, mapping=bike)
    i += 1
    pass
p.execute()
print("start index creation")

# Create an index
indexDefinition = IndexDefinition(
    prefix=["bike:"],
    index_type=IndexType.HASH,
)

conn.ft("bikes:idx").create_index(
    (
        TextField("model", no_stem=True, sortable=True),
        TagField("type"),
        NumericField("price", sortable=True),
        VectorField("description_embeddings", "FLAT", {"TYPE": "FLOAT32", "DIM": 768, "DISTANCE_METRIC": "COSINE"})
    ),
    definition=indexDefinition
)

print("start query")
# Query for a keyword/phrase
user_query = "Female specific mountain bike"

q = Query("*=>[KNN 3 @description_embeddings $vector AS result_score]")\
        .return_fields("result_score", "model", "type", "price", "description")\
        .sort_by("result_score", True)\
        .dialect(2)
bikes = conn.ft("bikes:idx").search(q, query_params={"vector": model.encode(user_query).astype(np.float32).tobytes()})

for bike in bikes.docs:
    print("********DOCUMENT:********")
    print("{} ({})".format(bike.model, bike.result_score))
    print(bike.description)

# Run a hybrid query
q = Query("(@type:{'Mountain Bikes'} @price:[3000 3500])=>[KNN 3 @description_embeddings $vector AS result_score]")\
        .return_fields("result_score", "model", "type", "price", "description")\
        .sort_by("result_score", True)\
        .dialect(2)
bikes = conn.ft("bikes:idx").search(q, query_params={"vector": model.encode(user_query).astype(np.float32).tobytes()})

for bike in bikes.docs:
    print("********DOCUMENT:********")
    print("{} ({})".format(bike.model, bike.result_score))
    print(bike.description)

