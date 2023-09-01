Id-generation:

We aren't using any auto-generated id-s in this article. Our id-s have a contextual meaning, which makes them more human-readable. An alternative implementation could use UUID-s or incremental counters for the purpose of the id generation.

Objects:

Buildings are stored as Hashes. The building type is represented as a textual value because we plan to use tag fields. The location is by intention not expressed via a Geoset because we will use RediSearch for this purpose later. References to other documents are represented as a String list (e.g., "a, b, c") because we are going to use a tag field for indexing purposes. Doing it this way does especially make sense if the cardinality of the 1-to-many relationship is quite low (so if we consider that a building has a comparatively small amount of work requests associated). The id of a work item is based on the request timestamp (plus a logical offset '#n'). The backward-association from the work item to the building is expressed within the key of the work item. However, I added specific reference fields (prefixed with ^) to support the search queries better. This is the same for the 1-to-1 relationship between the work request and the permit. We are using a simple UID as the id of a person. A person is also just stored as a Hash. There are two additional metadata fields _id and _type. The _id field represents the part of the id that can't be derived from other fields within the Hash.

The indices are prefixed with permits:v3 to distinguish it from the permits index that was used in the 'Introduction' section.

The type (constant value) is maintained as a tag. Key references are also implemented as tags. A detailed explanation about tags can be found here: https://oss.redislabs.com/redisearch/Tags/ . All the other string fields are kept as text, whereby we are disabling the stemming for fields that are not containing natural language (but for instance only names). The fields that have the type 'text' in our logical data model are stored as text fields with stemming enabled. We are using numeric fields for dates/times.
