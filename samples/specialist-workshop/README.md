# Specialist-Solutions-Workshops
this is putting real time workshop code into this running workshop environment
from [this github}(https://github.com/Redislabs-Solution-Architects/Specialist-Solution-Workshops/tree/main/Real-Time-Query-Workshop/python/)
the code used here needs a redis.ini file in the code directory as well as I made a simplified requirements.txt setup.   The rest can be copied over from the specialist github
### add requirements
```bash
docker exec -it jupyter pip install -r /home/jovyan/specialist-workshop/code/requirements.txt
```
### run all the programs
```bash
docker exec jupyter bash -c 'cd /home/jovyan/specialist-workshop/code; python all_labs.py'
```
