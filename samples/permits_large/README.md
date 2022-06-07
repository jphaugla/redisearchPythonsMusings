# Permits_large 
has python load scripts and data files
### unzip data file
```bash
gunzip data.csv.gz
```
### add requirements
```bash
docker exec -it jupyter pip install -r /home/jovyan/permits_large/requirements.txt
```
### load test files
```bash
docker exec -it jupyter python /home/jovyan/permits_large/import.py
```
### start up the cli through the redis container
```bash
docker exec -it redis redis-cli 
```
### have at it!
Run through the searches in queries.txt
