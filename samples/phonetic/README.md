# Phonetic related queries
Just a few examples on a few hash records
## Double Metaphone algorithm
'Metaphone' algorithm takes a word and applies a set of transformation rules to it, for example:

* Drop duplicate adjacent letters, except for C!
* If the word begins with 'KN', 'GN', 'PN', 'AE', 'WR', drop the first letter!
* Drop 'B' if it occurs after 'M' at the end of the word!

* add some cities hash records
```bash
redis-cli < add_textredis-cli < phonetics_idx.txt
```
* create index for records	
```bash
redis-cli < phonetics_idx.txt
```
* finally, run some queries out of *queries.txt*
