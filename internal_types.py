from typing import Any

# Record is a table row
Record = dict[str, Any] # Dict[str, Union[str, int, float, bool, None]]

# RowId is a unique identifier for a row
RowId = int

# ColumnName is the name of a column
ColumnName = str

# Word is a string of characters
Word = str

# Column
Columns = dict[ColumnName, type]

# Index is a column index
Index = dict[ColumnName, set[RowId]]

# InvertedIndex is a word index that maps a specific word to a set of row ids
InvertedIndex = dict[ColumnName, dict[Word, set[RowId]]]
