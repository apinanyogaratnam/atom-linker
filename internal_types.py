from typing import Any, Dict

# Record is a table row
Record = dict[str, Any]

# RowId is a unique identifier for a row
RowId = int

# ColumnName is the name of a column
ColumnName = str

# Word is a string of characters
Word = str

# Column
Columns = Dict[ColumnName, type]
