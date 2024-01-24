You task is to write Python program solutions to the given questions about tables.


## Example
**Question**
in eastern ontario, what percent of french-language workers have worked in the restaurant and food services sector?
**Table**
File: data/hitab/tables/hmt/100.json
Preview: agri-food industry sub-groups for workers aged 15 years and over, two agricultural regions of ontario, 2011
|                                                       |   ('eastern ontario', 'french-language workers') |   ('eastern ontario', 'other workers') |   ('northern ontario', 'french-language workers') |   ('northern ontario', 'other workers') |
|:------------------------------------------------------|-------------------------------------------------:|---------------------------------------:|--------------------------------------------------:|----------------------------------------:|
| ('percent', 'input and service supply')               |                                              2.9 |                                    2.1 |                                               2.9 |                                     1.3 |
| ('percent', 'food, beverage, and tobacco processing') |                                              9.7 |                                    6   |                                               3   |                                     3.3 |
| ('percent', 'food retail and wholesale')              |                                             35.3 |                                   31.3 |                                              39.1 |                                    37.3 |
| ('percent', 'food service')                           |                                             52.1 |                                   60.6 |

**Solution**
```python
df = parse_table("data/hitab/tables/hmt/100.json")
ontario_df = df[("eastern ontario", "french-language workers")]
percent = ontario_df.loc[("percent", "food service")]
print(percent)
```
**Tools**
```python
from toolbox import parse_table
```


## Example
**Question**
${question}
**Table**
${table}

**Solution**

