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

NOTES:

- unique indexes are when you want to make sure that the value is unique and indexed (possibly just make it unique without indexes? would be a set of items and make sure the item is not in the set. this way there will only be one index check for the CRUD stuff)

# delete all sorter.py.log files in git history

git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch sorter.py.log' --prune-empty --tag-name-filter cat -- --all
