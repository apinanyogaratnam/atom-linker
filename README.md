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


TODO:
- text search using elasticsearch or sphinx data structures
- consider using generators
- for indexes, add it sorted? might need to define a separate index attribute for sorted indexing
- create record type

NOTES:
- unique indexes are when you want to make sure that the value is unique and indexed (possibly just make it unique without indexes? would be a set of items and make sure the item is not in the set. this way there will only be one index check for the CRUD stuff)


# delete all sorter.py.log files in git history
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch sorter.py.log' --prune-empty --tag-name-filter cat -- --all
