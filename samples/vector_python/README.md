# Vector_python 
has python load scripts and data files
### add requirements
```bash
docker exec -it jupyter pip install -r /home/jovyan/vector_python/requirements.txt
```
### load test files
```bash
docker exec -it jupyter python /home/jovyan/vector_python/import.py
```
### start up the cli through the redis container
```bash
docker exec -it redis redis-cli 
```
### have at it!
Run a VSS query
```bash
redis-cli < vss_query.txt
```
