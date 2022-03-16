# fileload has python load scripts as well as phonetics, fuzzy, and slop queries
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
