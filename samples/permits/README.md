# Permits related queries
Just a few examples on a few hash records
* add some permits hash records
```bash
redis-cli < add_hash_permits.txt
```
* create index for records	
```bash
redis-cli < permits_idx.txt
```
* finally, run some queries out of *queries.txt*
* note:  can also run these queries against the larger permits_large dataset
moodle introduction quickstart

#  JSON permits
```bash
redis-cli < add_json_permits.txt
```
* create index for records	
```bash
redis-cli < permits_json_idx.txt
```
* then, run some queries out of *json_queries.txt*

* extra credit!   run auto_complete example
```bash
redis-cli < auto_complete.txt
```
