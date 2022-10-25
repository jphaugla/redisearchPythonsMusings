# pythonOM
has python and requirements files for this [redisOM github example](https://github.com/redis/redis-om-python)
### add requirements
```bash
docker exec -it jupyter pip install -r /home/jovyan/pythonOM/requirements.txt
```
### load test files
```bash
docker exec -it jupyter python /home/jovyan/pythonOM/main.py
```
### start up the cli through the redis container
```bash
docker exec -it redis redis-cli 
```
