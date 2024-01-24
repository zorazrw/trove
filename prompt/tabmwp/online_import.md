You task is to write Python program solutions to the given questions about tables.
The toolbox section lists all the available functions that can be used in your solution.


## Example
**Question**
Some friends discussed the sizes of their coin collections. What is the mean of the numbers?
**Table**
Name: Coin collections
Unit: None
Content:
| Name | Number of coins |
|  --- | --- |
| Braden | 76 |
| Camilla | 94 |
| Rick | 86 |
| Mary | 84 |
| Hector | 80 |
| Devin | 83 |
| Emily | 82 |
| Avery | 87 |

**Toolbox**
```python
# Import pandas functions
import pandas as pd
```
```python
# Find the mean of values in the specified data column.
find_mean(df: pd.DataFrame, value_column: str) -> float
```

**Solution**
```python
df = pd.DataFrame({
    'Name': ['Braden', 'Camilla', 'Rick', 'Mary', 'Hector', 'Devin', 'Emily', 'Avery'],
    'Number of coins': [76, 94, 86, 84, 80, 83, 82, 87]
})
mean_coins = find_mean(df, value_column="Number of coins")
print(mean_coins)
```
**Tools**
```python
import pandas as pd
from toolbox import find_mean
```


## Example
**Question**
${question}
**Table**
${table}

**Toolbox**
${toolbox}

**Solution**
