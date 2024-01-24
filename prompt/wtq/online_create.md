You task is to write Python program solutions to the given questions about tables.
You should also create Python functions that can be used by your solution, if you believe the function can be reused to solve other questions.


## Example
**Question**
how many people were murdered in 1940/41?
**Table**
File: 'csv/204-csv/149.tsv'
Preview: 
| Description Losses | 1939/40 | 1940/41 | Total |
| ------------------ | ------- | ------- | ----- |
| Direct War Losses | 360,000 |  | 543,000 |
| Murdered | 75,000 | 100,000 | 506,000 |
| Total | 504,000 | 352,000 | 2,770,000 |

**Solution**
```python
df = pd.read_table("data/wtq/csv/204-csv/149.tsv")
num_people = get_value_by_condition(df, condition_column="Description Losses", condition="Murdered", value_column="1940/41")
print(num_people)
```
**Tools**
```python
import pandas as pd

def get_value_by_condition(df, condition_column: str, condition: any, value_column: str) -> any:
    """"Get value that satisfies a condition in the specified column."""
    row = df[df[condition_column] == condition]
    return row[value_column].values[0]
```


## Example
**Question**
${question}
**Table**
${table}

**Solution**
