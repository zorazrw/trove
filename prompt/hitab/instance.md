Your task is to write the solution with high-level tools, i.e., Python functions, to answer question about tables.
Think about the potential program solution for this example, you can create high-level functions, that could be used to solve this example. For example, if the solution involves multiple actions that are always used together, it is more efficient to create and use the tool.

**Toolbox**
${toolbox}


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


**Question**
how many percent of university graduates among second-generation black women who originated from jamaica was higher than that of men in 2016?
**Table**
File: '1004.json'
Preview:
percentage of canadian-born black immigrants aged 25 to 59 with a postsecondary diploma, by sex and region or country of ancestry, 2016
|                                                       | ('women', 'non-university or university postsecondary diploma')   | ('women', 'university degree only')   | ('men', 'non-university or university postsecondary diploma')   | ('men', 'university degree only')   |
|:------------------------------------------------------|:------------------------------------------------------------------|:--------------------------------------|:----------------------------------------------------------------|:------------------------------------|
| ('region of ancestry', nan)                           | percent                                                           | percent                               | percent                                                         | percent                             |
| ('region of ancestry', 'caribbean and latin america') | 78.1                                                              | 34.8                                  | 59.5                                                            | 18.4                                |
| ('region of ancestry', 'africa')                      | 79.6                                                              | 50.8                                  | 63.6                                                            | 35.3                                |
| ('region of ancestry', 'other regions')               | 59.8                                                              | 19.1                                  | 46.8                                                            | 14.1                                |
| ('country of ancestry', nan)
**Solution**
```python
df = parse_table("data/hitab/tables/hmt/1004.json")
left_index = ("country of ancestry", "jamaica")
top_index_women = ('women', 'university degree only')
top_index_men = ('men', 'university degree only')
percent_higher = diff_by_top(df, left_index, top_index_women, top_index_men)
print(percent_higher)
```
**Tools**
```python
import pandas as pd

def diff_by_top(df: pd.DataFrame, left_index: tuple[str], top_index_1: tuple[str], top_index_2: tuple[str]) -> any:
    """Calculate the difference in values by locating index.
    """
    data_1 = df.loc[left_index, top_index_1]
    data_2 = df.loc[left_index, top_index_2]
    diff = data_1 - data_2
    return diff
```


**Question**
${question}
**Table**
${table}
**Solution**

