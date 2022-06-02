# Permits multi-level related queries
## Overview
* One index or multiple indices. 
  *  most natural decision would be to create one index per 
  * RediSearch DOESN'T allow you to query across indices. 
  * Search queries are limited to the scope of a single index.
* One index per type: Each type is represented by exactly one index. 
  * Need multiple independent search queries to perform combined searches. 
  * Advantage - index as it is without data duplication to support combined queries.
* All types are covered by a single index: There is one search index that covers the fields of all types. 
  * Must create hashes containing all fields for query. 
  * Could lead to a serious duplication of data.
* Aggregates approach - nest objects within each other
  * Create aggregate objects with multiple entities
  * For example, the Permit entity can be nested in the Work entity as a 1-1 relationship, and the Work entity can be nested in the Building entity as a 1-n relationship. 
  * This nesting done with RedisJSON not Hashes 
  * RediSearch does not support indexing of multi-values (scalar values or objects nested in arrays), with the exception of TAGs.

Just a few examples on a few hash records
* add some permits has records
```bash
redis-cli < add_hash_permits.txt
```
* create index for records	
```bash
redis-cli < permits_idx.txt
```
* finally, run some queries out of *queries.txt*

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

moodle data modelling basics

