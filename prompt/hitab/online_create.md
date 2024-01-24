You task is to write Python program solutions to the given questions about tables.
You should also create Python functions that can be used by your solution, if you believe the function can be reused to solve other questions.


## Example
**Question**
in eastern ontario, what percent of french-language workers have worked in the restaurant and food services sector?
**Table**
File: data/hitab/tables/hmt/100.json
Preview:
|                                                       |   ('eastern ontario', 'french-language workers') |   ('eastern ontario', 'other workers') |   ('northern ontario', 'french-language workers') |   ('northern ontario', 'other workers') |
|:------------------------------------------------------|-------------------------------------------------:|---------------------------------------:|--------------------------------------------------:|----------------------------------------:|
| ('percent', 'input and service supply')               |                                              2.9 |                                    2.1 |                                               2.9 |                                     1.3 |
| ('percent', 'food, beverage, and tobacco processing') |                                              9.7 |                                    6   |                                               3   |                                     3.3 |
| ('percent', 'food retail and wholesale')              |                                             35.3 |                                   31.3 |                                              39.1 |                                    37.3 |
| ('percent', 'food service')                           |                                             52.1 |                                   60.6 |

**Solution**
```python
df = parse_table("data/hitab/tables/hmt/100.json")
percent = get_data_cell(df, left_index=("percent", "food service"), top_index=("eastern ontario", "french-language workers"))
print(percent)
```
**Tools**
```python
from toolbox import parse_table
```
```python
import pandas as pd

def get_data_cell(df: pd.DataFrame, left_index: tuple[str], top_index: tuple[str]) -> any:
    """Locate the data cell in multi-index dataframe by left and top index.
    """
    data = df.loc[left_index, top_index]
    return data
```


## Example
**Question**
${question}
**Table**
${table}

**Solution**

