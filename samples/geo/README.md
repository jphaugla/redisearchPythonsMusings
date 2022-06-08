# Cities related queries
Just a few examples on a few hash records
* add some cities hash records
```bash
redis-cli < add_cities.txt
```
* create index for records	
```bash
redis-cli < citiesjidx.txt
```
* finally, run some queries out of *queries.txt*
