# Specialist-Solutions-Workshops
this is putting real time workshop code into this running workshop environment
from [this github}(https://github.com/Redislabs-Solution-Architects/Specialist-Solution-Workshops/tree/main/Real-Time-Query-Workshop/python/code)
### add requirements
```bash
docker exec -it jupyter pip install -r /home/jovyan/specialist-workshop/requirements.txt
```
### create schema for phonetic test
```bash
redis-cli < create_idx.txt
```
### load test files
```bash
docker exec -it jupyter python /home/jovyan/fileload/fileLoad.py
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
ft.search myIndex @body:Jon return 1 body
```
no match on John
```bash
ft.search myIndex @body:John return 1 body
```
phonetic insertion match on John
```bash
ft.search myIndex @phoneticBody:John return 1 phoneticBody
```
fuzzy match on John
```bash
ft.search myIndex @body:"%John%" return 1 body
```

no match on Cristina
```bash
ft.search myIndex @body:Cristina return 1 body
```
match on Christina
```bash
ft.search myIndex @body:Christina return 1 body
```
phonetic deletion match on Cristina
```bash
ft.search myIndex @phoneticBody:Cristina return 1 phoneticBody
```
fuzzy match on Cristina
```bash
ft.search myIndex @body:"%Cristina%" return 1 body
```

Cathy is not found
```bash
ft.search myIndex @body:Cathy return 1 body
```
Kathy is found
```bash
ft.search myIndex @body:Kathy return 1 body
```
phonetic substitution Cathy is found
```bash
ft.search myIndex @phoneticBody:Cathy return 1 phoneticBody
```
fuzzy match on Cathy
```bash
ft.search myIndex @body:"%Cathy%" return 1 body
```

Mike is found
```bash
ft.search myIndex @body:Mike return 1 body
```
Michael is not found
```bash
ft.search myIndex @body:Michael return 1 body
```
nickname phonetic Michael is still not found
```bash
ft.search myIndex @phoneticBody:Michael return 1 phoneticBody
```
Michael would need a synonym

Robert is found
```bash
 ft.search myIndex @body:Robert return 1 body
```

Robertson is not found
Robertson phonetic truncated name is found
```bash
ft.search myIndex @phoneticBody:Robertson return 1 phoneticBody
```
Robertson found with 3 level fuzzy
```bash
ft.search myIndex @body:"%%%Robertson%%%" return 1 body
```
Catherine is found
```bash
ft.search myIndex @body:Catherine return 1 body
```
Kathryn is not found
```bash
ft.search myIndex @body:Kathryn return 1 body
```
Kathryn phonetic is found
```bash
ft.search myIndex @phoneticBody:Kathryn return 1 phoneticBody
```

David Charles Butler  is one match regardless
```bash
ft.search myIndex @body:"David Charles Butler" return 1 body
```
David Butler is two matches
```bash
ft.search myIndex @body:"David Butler" return 1 body
```
David Butler with slop 0 is one match
```bash
ft.search myIndex @body:"David Butler" slop 0 return 1 body
```

Jesse James is found (even though data is James Jesse
```bash
ft.search myIndex @body:"Jesse James" return 1 body
```
slop 0 does not stop it
```bash
ft.search myIndex @body:"Jesse James" slop 0 return 1 body
```
slop 0 with INDORDER takes care of it
```bash
ft.search myIndex @body:"Jesse James" slop 0 INORDER return 1 body
```
Jaonna found with regular
```bash
ft.search myIndex @body:Jaonna return 1 body
```
Jaonna not found
```bash
ft.search myIndex @body:Joanna return 1 body
```
Jaonna found with phonetic
```bash
ft.search myIndex @phoneticBody:Joanna return 1 phoneticBody
```
Jaonna found with fuzzy
```bash
ft.search myIndex @body:%%Joanna%% return 1 body
```
Some simple queries
```bash
FT.SEARCH myIndex @body:selling|spelling|Jesse return 1 body
FT.SEARCH  myIndex @body:"wich erors" return 1 body
```
