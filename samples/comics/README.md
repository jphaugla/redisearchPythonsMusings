# Scoring and Relevancy example
## Redis University Link
* [Redis University Link](https://university.redis.com/courses/course-v1:redislabs+RU201+SP_2019_01/courseware/f00cc60d5c1b4e97bdf2eda8f8481e3d/8b573964589f4dee8aef9251a4aea87b/)
* [text transcript file included from the redis university training as well](file://transcript.txt)
* Create Index
```bash
redis-cli < create_idx.txt
```
* Add two non-weighted records
```bash
redis-cli < add_comics.txt
```
* search using keys *hero*
```bash
redis-cli < queries.txt
```
The resulting relevancy (score) tells us that Spiderman is a more likely hero than Batman because the word 'hero' appears more often for 'Spiderman' (term frequency). 
* modify the data to add a rating column and add superman
```bash
redis-cli < modify.txt
```
* Run same search again now with ratings considered
```bash
redis-cli < queries.txt
```
## now adding weights
```bash
redis-cli flushall
redis-cli < create_idx_rating.txt
redis-cli < add-comics2.txt
redis-cli < queries.txt
```
* run explainscore for more detail
```bash
redis-cli < queries_explain.txt
```
