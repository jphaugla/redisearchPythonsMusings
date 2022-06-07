import csv
import os
import redis
from redis.commands.search.field import TextField, TagField, NumericField, GeoField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
import time


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

if redis_password is not None:
    conn = redis.StrictRedis(redis_server, redis_port, password=redis_password,
                             decode_responses=True)
else:
    conn = redis.StrictRedis(redis_server, redis_port, decode_responses=True)
print("connect successful")

# Take a number String and convert it to Int
## If the passed value is an empty string then 0 is returned
def toInt(value):
    if value != "":
        tmp = value.replace(',','')
        return int(tmp.replace('.',''))
    else:
        return 0


# Take a longitude and latitude and convert it to a tuple
## If the passed values are empty strings then None is returned
def toGeoTuple(lng, lat):
    if lng != "" and lat != "":
        return '{},{}'.format(lng, lat)
    else:
        return None


    

# CSV Fields 
# ===========
# PERMIT_DATE,PERMIT_NUMBER,YEAR,MONTH_NUMBER,REPORT_PERMIT_DATE,JOB_CATEGORY,ADDRESS,LEGAL_DESCRIPTION,NEIGHBOURHOOD,NEIGHBOURHOOD_NUMBER,JOB_DESCRIPTION,BUILDING_TYPE,WORK_TYPE,FLOOR_AREA,CONSTRUCTION_VALUE,ZONING,UNITS_ADDED,LATITUDE,LONGITUDE,LOCATION,COUNT
#
# Schema
# ======

if CREATE_IDX == True:
    
    # RediSearch 2.0
    indexDefinition = IndexDefinition(prefix=['prm:'], index_type=IndexType.HASH)
    indexSchema = (
        NumericField("permit_timestamp", sortable=True),
        TextField("job_category", no_stem=True),
        TextField("address", no_stem=True),
        TagField("neighbourhood", sortable=True),
        TextField("description"),
        TextField("building_type", weight=20, no_stem=True, sortable=True),
        TextField("work_type", no_stem=True),
        NumericField("floor_area", sortable=True),
        NumericField("construction_value", sortable=True),
        TagField("zoning"),
        NumericField("units_added", sortable=True),
        GeoField("location")

    )
    # conn.execute_command("FT.CREATE", "permits", "ON", "HASH", "PREFIX", "1", "prm:", "SCHEMA", "permit_timestamp", "NUMERIC", "SORTABLE",
    #                     "job_category", "TEXT", "NOSTEM", "address", "TEXT", "NOSTEM", "neighbourhood", "TAG", "SORTABLE", "description", "TEXT",
    #                    "building_type", "TEXT", "WEIGHT", 20, "NOSTEM", "SORTABLE", "work_type", "TEXT", "NOSTEM", "SORTABLE", "floor_area", "NUMERIC", "SORTABLE",
    #                    "construction_value", "NUMERIC", "SORTABLE", "zoning", "TAG",  "units_added", "NUMERIC", "SORTABLE", "location", "GEO")
    print("before try on index creation")
    try:
        conn.ft(index_name="permits").create_index(indexSchema, definition=indexDefinition)
    except redis.ResponseError:
        conn.ft(index_name="permits").dropindex(delete_documents=False)
        conn.ft(index_name="permits").create_index(indexSchema, definition=indexDefinition)

with open('/home/jovyan/permits_large/data.csv' ) as f:
    reader = csv.DictReader(f)
    pipe = conn.pipeline()
    i = 0
    start = time.time()

    for row in reader:

        # Key and score
        key = row['PERMIT_NUMBER']
        score = 1.0

        # Mapped field values
        fields = {}
        permit_date = row['REPORT_PERMIT_DATE']
        fields['permit_timestamp'] = time.mktime(time.strptime(permit_date, "%m/%d/%Y %H:%M:%S %p"))
        fields['job_category'] = row['JOB_CATEGORY']
        fields['address'] = row['ADDRESS']
        fields['neighbourhood'] = row['NEIGHBOURHOOD']
        fields['description'] = row['JOB_DESCRIPTION']
        fields['building_type'] = row['BUILDING_TYPE']
        fields['work_type'] = row['WORK_TYPE']
        floor_area = row['FLOOR_AREA']
        fields['floor_area'] = toInt(floor_area)
        construction_value = row['CONSTRUCTION_VALUE']
        fields['construction_value'] = toInt(construction_value)
        fields['zoning'] = row['ZONING']
        units_added = row['UNITS_ADDED']
        fields['units_added'] = toInt(units_added)
        lat = row['LATITUDE']
        lng = row['LONGITUDE']
        location = toGeoTuple(lng, lat)
        if location != None:
            fields['location'] = location
    
        #print(fields)
        fieldsArr = []

        for k,v in fields.items():
            fieldsArr.append(k)
            fieldsArr.append(v)

        # RediSearch 2.0        
        fields['__score'] = score
        pipe.hmset("prm:{}".format(key), fields)

        # Execute every 500 commands
        if i % 500 == 0:
            print("Executing block {}".format(i))
            pipe.execute()
        
        i += 1
    
    # Execute the rest of the commands
    pipe.execute()
    end = time.time()

    print("The import took {} s.".format(end - start))

