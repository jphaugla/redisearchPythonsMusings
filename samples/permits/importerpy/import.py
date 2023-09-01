import csv
from redis import Redis
import time
import config

# Constants
FLUSH = True
CREATE_IDX = True

host = config.REDIS_CFG["host"]
port = config.REDIS_CFG["port"]
pwd = config.REDIS_CFG["password"]
redis = Redis(host=host, port=port, password=pwd, charset="utf-8", decode_responses=True)

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

if FLUSH == True:
    redis.flushdb()

if CREATE_IDX == True:
    
    # RediSearch 2.0
    redis.execute_command("FT.CREATE", "permits", "ON", "HASH", "PREFIX", "1", "prm:", "SCHEMA", "permit_timestamp", "NUMERIC", "SORTABLE", "job_category", "TEXT", "NOSTEM", "address", "TEXT", "NOSTEM", "neighbourhood", "TAG", "SORTABLE", "description", "TEXT", "building_type", "TEXT", "WEIGHT", 20, "NOSTEM", "SORTABLE", "work_type", "TEXT", "NOSTEM", "SORTABLE", "floor_area", "NUMERIC", "SORTABLE", "construction_value", "NUMERIC", "SORTABLE", "zoning", "TAG",  "units_added", "NUMERIC", "SORTABLE", "location", "GEO")

    # RediSearch 1.6
    # redis.execute_command("FT.CREATE", "permits", "SCHEMA", "permit_timestamp", "NUMERIC", "SORTABLE", "job_category", "TEXT", "NOSTEM", "address", "TEXT", "NOSTEM", "neighbourhood", "TAG", "SORTABLE", "description", "TEXT", "building_type", "TEXT", "WEIGHT", 20, "NOSTEM", "SORTABLE", "work_type", "TEXT", "NOSTEM", "SORTABLE", "floor_area", "NUMERIC", "SORTABLE", "construction_value", "NUMERIC", "SORTABLE", "zoning", "TAG",  "units_added", "NUMERIC", "SORTABLE", "location", "GEO")
    


with open('data.csv' ) as f:
    reader = csv.DictReader(f)
    pipe = redis.pipeline()
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

        # COMMAND: FT.ADD permits tst:permit:2 1 FIELDS "description" "To construct a loft" "construction_value" 42 building_type "apartment"
        # W/O PIPELINING: redis.execute_command("FT.ADD", "permits", key, score, "FIELDS", *fieldsArr)
        # W/ PIPELINING:

        # RediSearch 2.0        
        fields['__score'] = score
        pipe.hmset("prm:{}".format(key), fields)

        # RediSearch 1.6
        # pipe.execute_command("FT.ADD", "permits", key, score, "FIELDS", *fieldsArr)

        # Execute every 500 commands
        if i % 500 == 0:
            print("Executing block {}".format(i))
            pipe.execute()
        
        i += 1
    
    # Execute the rest of the commands
    pipe.execute()
    end = time.time()

    print("The import took {} s.".format(end - start))

