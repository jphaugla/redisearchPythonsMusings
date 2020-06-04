# redisearchPythonProductCatalog
A search product catalog solution based on icecat files
## Initial project setup
Get this github code
```bash 
get clone https://github.com/jphaugla/redisearchPythonProductCatalog.git
```
Two options for setting the environment are given:  
  * run with docker-compose using a flask and redis container
  * installing for mac os
docker-compose is much easier and is main method documented here
## docker compose startup
```bash
docker-compose up -d --build
```
## Code and File discussion
This is an implementation of a product Catalog using data download from
 [icecat](https://iceclog.com/open-catalog-interface-oci-open-icecat-xml-and-full-icecat-xml-repositories/)

### Download the datafiles to the data subdirectory
To download the datafiles, a free login id from icecat is required
Once effectively logged in to icecat need to retrieve these two files
  * https://data.Icecat.biz/export/freexml/refs/CategoriesList.xml.gz
  * https://data.icecat.biz/export/freexml/nl/files.index.xml.gz

### unzip data files
The data file directory is mapped 
using docker-compose volume to /data in flask container
```bash
cd data
unzip files.index.csv.zip
gunzip CategoriesList.xml.gz
```
### create schema
```bash
cd src
./createCatSchema.sh
redis-cli<createSchema.txt
```
### load categories
This is pretty quick-less than a minute
```bash
docker exec -it jupyter python /home/jovyan/scripts/categoryImport.py
```
### load Products
This can take quite a long time (maybe 25 minutes)
Loading over 1.2 million rows with a category name lookup for each product
```bash
docker exec -it jupyter python /home/jovyan/scripts/productImport.py
```
### Add python requirements
```bash
docker exec -it jupyter pip install -r /home/jovyan/scripts/requirements.txt
### run queries using queries.txt or run indivual queries from redis-cli
```bash
redis-cli  < scripts/queries.txt
```
#### from redis-cli
```bash
redis-cli 
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

