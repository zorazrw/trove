Your task is to write the solution with high-level tools, i.e., Python functions, to answer question about tables.
Think about the potential program solution for this example, you can create high-level functions, that could be used to solve this example. For example, if the solution involves multiple actions that are always used together, it is more efficient to create and use the tool.

**Toolbox**
${toolbox}


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
Gina kept track of how many laps she swam during the past 7 days. What is the range of the numbers?
**Table**
Name: Laps swum
Unit: None
Content:
| Day | Number of laps |
| --- | --- |
| Friday | 41 |
| Saturday | 38 |
| Sunday | 35 |
| Monday | 41 |
| Tuesday | 35 |
| Wednesday | 31 |
| Thursday | 38 |
**Solution**
```python
df = pd.DataFrame({
    'Day': ['Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'],
    'Number of laps': [41, 38, 35, 41, 35, 31, 38]
})
range_laps = find_range(df, value_column="Number of laps")
print(range_laps)
```
**Tools**
```python
import pandas as pd

def find_range(df: pd.DataFrame, value_column: str) -> int:
    """
    Find the range (max - min) of values in the specified data column.
    Args:
        df: pandas DataFrame object, contain table info.
        value_column: str, name of the column containing the values.
    Rets:
        int: The range of the values.
    """
    # get the minimum and maximum values in the column
    min_value = df[value_column].min()
    max_value = df[value_column].max()
    # calculate the range
    range_value = max_value - min_value
    return range_value
```


## Example
**Question**
${question}
**Table**
${table}
**Solution**
