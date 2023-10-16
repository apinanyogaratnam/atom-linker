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
TODO: - need to look at elasticsearch and sphinx infrastructure for ideas
- need to be able to do full matches as well

TODO:
- text search using elasticsearch or sphinx data structures
- consider using generators
- for indexes, add it sorted? might need to define a separate index attribute for sorted indexing
- can trees be used in this db?

NOTES:
- unique indexes are when you want to make sure that the value is unique and indexed (possibly just make it unique without indexes? would be a set of items and make sure the item is not in the set. this way there will only be one index check for the CRUD stuff)


# delete all sorter.py.log files in git history
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch sorter.py.log' --prune-empty --tag-name-filter cat -- --all
