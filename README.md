# redisearchPythonProductCatalog
A search product catalog solution based on icecat files
#### the autosuggest code and entire UI is shamelessly stolen from [redisearch fortune 500 companies](https://github.com/Redislabs-Solution-Architects/redis_autocomplete_python)
## Initial project setup
Get this github code
```bash 
get clone https://github.com/jphaugla/redisearchPythonProductCatalog.git
```
This github is setup to run with docker-compose using a jupyter and redis container
## docker compose startup
```bash
docker-compose up -d 
```
## Code and File discussion
This is an implementation of a product Catalog using data download from
 [icecat](https://iceclog.com/open-catalog-interface-oci-open-icecat-xml-and-full-icecat-xml-repositories/)

### Download the datafiles to the data subdirectory
To download the datafiles, a free login id from icecat is required
Once effectively registed to icecat need to retrieve these two files using the registered username and password.  The quotes are needed.
```bash
curl -u 'yourUN':'yourPW' https://data.Icecat.biz/export/freexml/refs/CategoriesList.xml.gz -o CategoriesList.xml.gz
curl -u 'yourUN':'yourPW' https://data.Icecat.biz/export/freexml/files.index.csv.gz -o files.index.csv.gz
```

### unzip data files
The data file directory is mapped 
using docker-compose volume to /data in flask container
```bash
cd data
gunzip files.index.csv.gz
gunzip CategoriesList.xml.gz
```
### create schema
```bash
docker exec -i redis bash <<EOF
redis-cli < /src/createSchema.txt
redis-cli < /src/createCatSchema.txt
exit
EOF
```
### Add python requirements
```bash
docker exec -it jupyter pip install -r /home/jovyan/scripts/requirements.txt
```
### load categories
This is pretty quick-less than a minute
The redis node and port can be changed. The python code uses 2 environment variable REDIS_SERVER and REDIS_PORT.  The default is REDIS_SERVER=redis and REDIS_PORT=6379

```bash
docker exec -it jupyter python /home/jovyan/scripts/categoryImport.py
```
### load Products
This can take quite a long time (maybe 25 minutes)
Loading over 1.2 million rows with a category name lookup for each product
```bash
The redis node and port can be changed. The python code uses 2 environment variable REDIS_SERVER and REDIS_PORT.  The default is REDIS_SERVER=redis and REDIS_PORT=6379
docker exec -it jupyter python /home/jovyan/scripts/productImport.py
```
### run queries  from redis-cli
#### from redis-cli (check for new queries in src/queries.txt)
```bash
docker exec -it redis redis-cli 
ft.search product * return 2 model_name prod_id
ft.search product @model_name:iphone return 2 model_name prod_id
ft.search product @m_supplier_name:HP return 2 model_name category_name
ft.search product @category_name:Calculators return 2 model_name country_market
ft.search product @category_name:Calculators@country_market:{GB} return 2 model_name country_market
exit
```
  * start flask app server
 ```bash
 docker exec -it jupyter python /home/jovyan/scripts/app.py
 ```
### test the website
 [localhost link](http://localhost:5000)
### create schema for phonetic test
```bash
docker exec -i redis bash <<EOF
/src/createDocSchema.sh
exit
EOF
```
### load test files
```bash
docker exec -it jupyter python /home/jovyan/scripts/fileLoad.py
```
### start up the cli through the redis container
```bash
docker exec -it redis redis-cli 
```
### have at it!

# sample queries
exact match
```bash
ft.search myIndex @body:"Haugland"
```

match on Jon
```bash
ft.search myIndex @body:Jon
```
no match on John
```bash
ft.search myIndex @body:John
```
phonetic insertion match on John
```bash
ft.search myIndex @phoneticBody:John
```
fuzzy match on John
```bash
ft.search myIndex @body:"%John%"
```

no match on Cristina
```bash
ft.search myIndex @body:Cristina
```
match on Christina
```bash
ft.search myIndex @body:Christina
```
phonetic deletion match on Cristina
```bash
ft.search myIndex @phoneticBody:Cristina
```
fuzzy match on Cristina
```bash
ft.search myIndex @body:"%Cristina%"
```

Cathy is not found
```bash
ft.search myIndex @body:Cathy
```
Kathy is found
```bash
ft.search myIndex @body:Kathy
```
phonetic substitution Cathy is found
```bash
ft.search myIndex @phoneticBody:Cathy
```
fuzzy match on Cathy
```bash
ft.search myIndex @body:"%Cathy%"
```

Mike is found
```bash
ft.search myIndex @body:Mike
```
Michael is not found
```bash
ft.search myIndex @body:Michael
```
nickname phonetic Michael is still not found
```bash
ft.search myIndex @phoneticBody:Michael
```
Michael would need a synonym

Robert is found
```bash
 ft.search myIndex @body:Robert
```

Robertson is not found
Robertson phonetic truncated name is found
```bash
ft.search myIndex @phoneticbody:Robertson
```
Robertson found with 3 level fuzzy
```bash
ft.search myIndex @body:"%%%Robertson%%%"
```
Catherine is found
```bash
ft.search myIndex @body:Catherine
```
Kathryn is not found
```bash
ft.search myIndex @body:Kathryn
```
Kathryn phonetic is found
```bash
ft.search myIndex @phoneticbody:Kathryn
```

David Charles Butler  is one match regardless
```bash
ft.search myIndex @body:"David Charles Butler"
```
David Butler is two matches
```bash
ft.search myIndex @body:"David Butler"
```
David Butler with slop 0 is one match
```bash
ft.search myIndex @body:"David Butler" slop 0
```

Jesse James is found (even though data is James Jesse
```bash
ft.search myIndex @body:"Jesse James"
```
slop 0 does not stop it
```bash
ft.search myIndex @body:"Jesse James" slop 0
```
slop 0 with INDORDER takes care of it
```bash
ft.search myIndex @body:"Jesse James" slop 0 INORDER
```
Joanna found with regular
```bash
ft.search myIndex @body:Joanna
```
Jaonna not found
```bash
ft.search myIndex @body:Joanna
```
Jaonna found with phonetic
```bash
ft.search myIndex @phoneticBody:Joanna
```
Jaonna found with fuzzy
```bash
ft.search myIndex @body:%%Joanna%%
```
Some simple queries
```bash
FT.SEARCH myIndex @body:selling|spelling|Jesse
FT.SEARCH  myIndex @body:"wich erors"
```
