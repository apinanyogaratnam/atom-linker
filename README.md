# Atom Linker

Atom Linker is a relational database that is suited for text search. This was inspired by
the optimizations and relations postgresql provides and the text search capabilities of
elasticsearch. This database currently runs on memory only at the moment.
There is no third party packages used in this repo. This is a pure python implementation.
This database allows for reading while indexes are being built but reads will be slower
until the index is finished building (similar to CONCURRENTLY in postgres when creating indexes).


<!--
- indexes
- relations (pk and fk)
- locks
- stats
- disk storage
- network
- json storage

# Notes for fk implementation

- fk is related to pk which is only by the id for current implementation
- fk can only be added after the column is created
- fk can only be type of int

# Notes for text search implementation

- text search is only for string columns, must make sure to raise errors if the column user is trying to add index for is not a string
- using inverted indexes for fast searches
- need to use sets for list of row ids
- need to look at elasticsearch and sphinx infrastructure for ideas: https://www.youtube.com/watch?v=fcIzAg63WyI&t=38s
- need to be able to do full matches as well
- search types: https://chat.openai.com/c/f0ec05f9-0d97-4774-8699-3a3548a4c398

TODO:

- extended functionalities:
    - store logs of data metrics
    - key,value store
    - graph db store
    - trees store (all kinds of trees)
    - storing data in memory and on disk
    - storing unstructured data i.e. json
    - ordered sets/arrays
    - sets
    - queues

- aggregate functions like sum, avg, min, max, etc.
- aggregate functions but it will be always precomputed i.e. when a row is inserted, the aggregate functions will be updated in the background
- hyperloglog for unique counts:
    - https://www.youtube.com/watch?v=lJYufx0bfpw
    - https://chat.openai.com/c/f9947e04-d811-4ef5-9245-d7702e223140
    - https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf
    - https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/40671.pdf
- need to save all data to disk in an efficient way maybe something like mapping record ids to filenames in json or something and this needs to be handled in an async way
- consider sequential threading for indexes (sequential transactions)
- add 'row level locking' so that if methods outside of the db are being threaded, then the db will not be affected
- use the wait from concurrent.futures to wait for all threads to finish before returning the data and i can have futures for each type of index so i can wait for all of them to complete
- a problem with get records by column is that if an index is being created, there is a likely chance that only some of the data is available in the index so the records being returned will not be the full list. might need to make sure no threads are active when creating the index or do something with is_index_being_built = True/False per column basis.
- need to save threads in the event of deleting an indexed column, need to know the running threads and then kill them safely?
- batch inserts
- return the row id as well when returning a list of records
- need to lowercase all strings before inverted indexing + removing punctuation and diacritics
- root word indexing: basically stemming where you remove the suffixes and prefixes of words to get the root word and then whenever a search is done, you remove the suffixes and prefixes of the search term and then search for the root word which will be indexes leading to more cases where the search term will be found in the index
- text search using elasticsearch or sphinx data structures
- consider using generators
- for indexes, add it sorted? might need to define a separate index attribute for sorted indexing
- can trees be used in this db?
- add types for all parameters where necessary / using already defined types
- fuzzy search: https://chat.openai.com/c/e89038e7-4cf9-4639-9573-9c57ea9c96c3
- separate out GET/POST/UPDATE/DELETE/INDEXES methods into its own class for each table (crud classes inherit from indexes, table inherit from crud classes)
- for indexes class, make utility methods instead of manually looking through the index attributes
- update ruff settings to stop converting Dict -> dict and fix all cases where dict should be Dict
- use default dictionaries
- use built in python functions/methods for optimal performance
- ask chatgpt for cleanup and optimization tips
- add threading and locks
- if a key is being used by a foreign key, then it cannot be deleted
- think if diacritics should be removed or not when doing sanitized search
- test this at massive scale (need to do millions of inserts and then do millions of searches, etc.)
- maybe do tokenized search with the inverted index?
- maybe do combinations of the words in the inverted index?
- look at my batchrequest package i made?
- need to add a way to create a table from a csv file
- add locks for all indexes and make them threaded
- might need autovacuuming since the indexes can still exist even if the row is deleted. maybe save the threads that are running in self.running_indexes_threads and then when the index is deleted, check if the thread is in self.running_indexes_threads and if it is, then kill the thread safely and then delete the index
- consider using multiprocessing instead of threading
- might be an issue with having both index and unique index for the same column
- need to error handle i.e. try catch and if any errors occur, handle the errors, make sure to shutdown tables if need be
- for the server, might need to find something super fast or use grpc with strictly using strings to allow for any types. might just end up making our own protocol based on TCP.
- security i.e. usernames, database names, passwords, ports; SSL i.e. encrypted data when transferring data between networks
- listen/notify (probably need to experiment with real time data project to better understand this)
- prepared statements?
- partitioning?
- have some sort of ordering for fast binary search
- use .get instead of [] for dicts for faster performance
- ability to store documents i.e. document db like amazon s3 + ability to only return chunks of the document so that the entire document is not loaded into memory at once
- store blobs? binary large objects

NOTES:

- unique indexes are when you want to make sure that the value is unique and indexed (possibly just make it unique without indexes? would be a set of items and make sure the item is not in the set. this way there will only be one index check for the CRUD stuff)

# delete all sorter.py.log files in git history

git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch sorter.py.log' --prune-empty --tag-name-filter cat -- --all


# THIS PR:
- create threads to save data to disk after insert/update/delete data + indexes

-->
