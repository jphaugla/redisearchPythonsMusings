# redisearchPythonsMusings
The product category part of this has been superseded by a new combined JSON and search version [redis JSON and Search](https://github.com/jphaugla/redisJSONProductCatalog)
## helpful links
* [redisearch 2.0 getting started blog](https://redis.com/blog/getting-started-with-redisearch-2-0/)
* [redisearch 2.0 getting started github](https://github.com/RediSearch/redisearch-getting-started)
* [redisearch documentation](https://oss.redis.com/redisearch/master/)
* [redisearch github](https://github.com/Redislabs-Solution-Architects/redisaml#example-redisearch-queries)
* [redisearch sample query github](https://github.com/Redislabs-Solution-Architects/contracts#sample-queries)
* [redisearch client libraries](https://github.com/RediSearch/RediSearch#client-libraries)
* [another redisearch client libraries](https://oss.redis.com/redisearch/Clients/)

## Initial project setup
Get this github code
```bash 
get clone https://github.com/jphaugla/redisearchPythonsMusings.git
```
This github is setup to run with docker-compose using a jupyter and redis container
## docker compose startup
```bash
docker-compose up -d 
```
There is a separate readme for each example under the samples directory-check it out!
NOTE:   can run these queries using the redis-cli in the docker container or with a locally installed redis-cli
since the docker redis container is running on port 6379, no paramters are needed on the redis-cli command
```bash
redis-cli set hello world
redis-cli get hello
docker exec -it redis redis-cli set hello world
docker exec -it redis redis-cli get hello
```
## Samples 
* [Comics - relevancy and scoring](samples/comics/README.md)
* [Fileload - python phonetics, fuzzy, and slop](samples/comics/README.md)
* [Movies - Large number of search queries and aggregations](samples/movies/README.md)
* [People - Few queries including fuzzy](samples/people/README.md)
* [Permits - Few queries including and/or as well as tags](samples/permits/README.md)
* [Permits_multi - Data modeling issues with single or multiple indexes](samples/permits_multi/README.md)
* [Premium - shows multiple prefixes and Filter on create index](samples/premium/README.md)
* [tagsVsText - shows tagging and text with hashes and json](samples/tagsVsText/README.md)
