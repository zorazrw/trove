You task is to write Python program solutions to the given questions about tables.
You should also create Python functions that can be used by your solution, if you believe the function can be reused to solve other questions.


## Example
**Question**
To figure out how many vacation days he had left to use, Austin looked over his old calendars to figure out how many days of vacation he had taken each year. According to the table, what was the rate of change between 2015 and 2016?
**Table**
Name: Vacation days taken by Austin
Unit: vacation days per year
Content:
| Year | Vacation days |
| --- | --- |
| 2013 | 23 |
| 2014 | 18 |
| 2015 | 11 |
| 2016 | 15 |
| 2017 | 8 |

**Solution**
```python
df = pd.DataFrame({
    'Year': [2013, 2014, 2015, 2016, 2017],
    'Vacation days': [23, 18, 11, 15, 8]
})
rate = rate_of_change(df, value_column="Vacation days", time_column="Year", time1=2015, time2=2016)
print(rate)
```

**Tools**
```python
import pandas as pd

def rate_of_change(df: pd.DataFrame, value_column: str, time_column: str, time1: int, time2: int) -> float:
    """Calculate the rate of change in values between two times."""
    # get the row for each time stamp
    time1_row = df[df[time_column] == time1]
    time2_row = df[df[time_column] == time2]
    # get the number of games won for each time
    time1_value = time1_row[value_column].values[0]
    time2_value = time2_row[value_column].values[0]
    # calculate the rate of change
    rate_of_change = (time2_value - time1_value) / (time2 - time1)
    return rate_of_change
```


## Example
**Question**
${question}
**Table**
${table}

**Solution**
