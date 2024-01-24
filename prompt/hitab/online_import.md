You task is to write Python program solutions to the given questions about tables.
The toolbox section lists all the available functions that can be used in your solution.


## Example
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

**Toolbox**
```python
# Import pandas functions
import pandas as pd
```
```python
# Count the number of entries satisfying a condition
count_by_condition(df, condition_column: str, condition_value: any)
```

**Solution**
```python
df = pd.read_table("data/wtq/csv/203-csv/463.tsv")
num_canada_films= count_by_condition(df, condition_column="Language", condition_value="Kannada")
print(num_kannada_films)
```
**Tools**
```python
import pandas as pd
from toolbox import count_by_condition
```


## Example
**Question**
${question}
**Table**
${table}

**Toolbox**
${toolbox}

**Solution**

