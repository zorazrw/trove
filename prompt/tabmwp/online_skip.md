You task is to write Python program solutions to the given questions about tables.

## Example
**Question**
This is Franco's complete financial record for September. At the end of September, how much money did Franco have?
**Table**
Name: None
Unit: $
Content:
| Date | Description | Received | Expenses | Available Funds |
|  --- | --- | --- | --- | --- |
|  | Balance: end of August | | | $29.20 |
| 9/2 | sandpaper | | $2.45 | $26.75 |
| 9/3 | paintbrush | | $5.95 | $20.80 |
| 9/5 | painting fence | $30.00 | | $50.80 |

**Solution**
```python
df = pd.DataFrame({
    'Date': ['9/2', '9/3', '9/5'],
    'Description': ['sandpaper', 'paintbrush', 'painting fence'],
    'Received': [None, None, 30.00],
    'Expenses': [2.45, 5.95, None],
    'Available Funds': [26.75, 20.80, 50.80]
})
available_funds = df["Available Funds"].values[-1]
print(available_funds)
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
