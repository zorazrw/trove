Your task is to use tools, i.e., Python functions, to answer question about tables.
Write a program solution to the question by decomposing it into multiple steps. Then specify the tools used in each step by importing from the toolbox. Make sure that all tools used in the solution are defined in the toolbox. Do not use any undefined functions.
You can use functions in numpy, pandas if they help. Each table is presented in markdown format, you can transform tables into pandas DataFrame objects. Each table is stored in a tsv file, you can transform tables into pandas DataFrame objects.

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
murdered_row = df[df["Description Losses"] == "Murdered"]
num_people = murdered_row["1940/41"].values[0]
print(num_people)
```
**Tools**
```python
import pandas as pd
```


**Question**
does pat or john have the highest total?
**Table**
File: 'csv/204-csv/925.tsv'
Preview:
| Name | League | FA Cup | Total |
| ---- | ------ | ------ | ----- |
| Danny Coles | 3 | 0 | 3 |
| John O'Flynn | 11 | 0 | 12 |
| Pat Baldwin | 1 | 0 | 1 |
| Total | 0 | 0 | 0 |
**Solution**
```python
df = pd.read_table("data/wtq/csv/204-csv/925.tsv")
name_list = ["Pat Baldwin", "John O'Flynn"]
name_df = df[df["Name"].isin(name_list)]
highest_total = name_df["Total"].max()
highest_row = name_df[name_df["Total"] == highest_total]
name_highest = highest_row["Name"].values[0]
print(name_highest)
```
**Tools**
```python
import pandas as pd 
```


**Question**
${question}
**Table**
${table}
**Solution**
