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
