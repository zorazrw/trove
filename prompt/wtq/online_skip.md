You task is to write Python program solutions to the given questions about tables.


## Example
**Question**
what match comes after gl-b-5?

**Table**
File: data/wtq/csv/204-csv/896.tsv
Preview: 
| Match | Opponents | Score |
|  --- | --- | --- |
| GL-B-1 | [[]] | - |
| GL-B-5 | [[]] | - |
| Quarterfinals-1 | [[]] | - |
| Quarterfinals-2 | [[]] | - |

**Solution**
```python
df = pd.read_table("data/wtq/csv/204-csv/896.tsv")
match_row = df[df["Match"] == "GL-B-5"]
next_match_index = match_row.index[0] + 1
next_match = df.loc[next_match_index, "Match"]
print(next_match)
```
**Tools**
```python
import pandas as pd
```


## Example
**Question**
${question}
**Table**
${table}

**Solution**
