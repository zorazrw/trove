Your task is to write the solution with high-level tools, i.e., Python functions, to answer question about tables.
Think about the potential program solution for this example, you can create high-level functions, that could be used to solve this example. For example, if the solution involves multiple actions that are always used together, it is more efficient to create and use the tool.

**Toolbox**
${toolbox}


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


**Question**
what is the total number of films with the language of kannada listed?
**Table**
File: data/wtq/csv/203-csv/463.tsv
Preview: | Year | Role | Language | Notes |
|  --- | --- | --- | --- |
| 2008 | Chanchala | Kannada | Filmfare Award for Best Actress - Kannada\nKarnataka State Film Award for Best Actress |
| 2009 | Kushi | Kannada | Filmfare Award for Best Actress - Kannada |
| 2010 | Geetha | Kannada | Filmfare Award for Best Actress - Kannada\nUdaya Award for Best Actress |
| 2011 | Gayithri | Kannada | Nominated, Filmfare Award for Best Actress – Kannada |
**Solution**
```python
df = pd.read_table("data/wtq/csv/203-csv/463.tsv")
num_canada_films= count_by_condition(df, condition_column="Language", condition="Kannada")
print(num_kannada_films)
```
**Tools**
```python
import pandas as pd

def count_by_condition(df, condition_column: str, condition: any) -> int:
    """Get number of rows that satisfy a condition in the specified column."""
    return len(df[df[condition_column] == condition])
```


**Question**
${question}
**Table**
${table}
**Solution**
