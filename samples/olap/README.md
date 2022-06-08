# OLAP related queries
Just a few examples on a few hash records
* add some city hash records
```bash
redis-cli < add_cities.txt
```
* create index for records	
```bash
redis-cli < cities_idx.txt
```
* finally, run some queries out of *queries.txt*
