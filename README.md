# redisearchPythonsMusings
#  the product category part of this has been superseded by a new combined JSON and search version [redis JSON and Search](https://github.com/jphaugla/redisJSONProductCatalog)
## helpful links
[redisearch 2.0 getting started blog](https://redis.com/blog/getting-started-with-redisearch-2-0/)
[redisearch 2.0 getting started github](https://github.com/RediSearch/redisearch-getting-started)
[redisearch documentation](https://oss.redis.com/redisearch/master/)
[redisearch github](https://github.com/Redislabs-Solution-Architects/redisaml#example-redisearch-queries)
[redisearch sample query github](https://github.com/Redislabs-Solution-Architects/contracts#sample-queries)

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
