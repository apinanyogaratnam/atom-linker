# Atom Linker

Atom Linker is a relational database that is suited for text search. This was inspired by
the optimizations and relations postgresql provides and the text search capabilities of
elasticsearch. This database currently runs on memory only at the moment.
There is no third party packages used in this repo.


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

NOTES:

- unique indexes are when you want to make sure that the value is unique and indexed (possibly just make it unique without indexes? would be a set of items and make sure the item is not in the set. this way there will only be one index check for the CRUD stuff)

# delete all sorter.py.log files in git history

git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch sorter.py.log' --prune-empty --tag-name-filter cat -- --all

-->
