Your task is to use tools, i.e., Python functions, to answer question about tables.
Write a program solution to the question by decomposing it into multiple steps. Then specify the tools used in each step by importing from the toolbox. Make sure that all tools used in the solution are defined in the toolbox. Do not use any undefined functions.
You can use functions in numpy, pandas if they help. Each table is presented in markdown format, you can transform tables into pandas DataFrame objects.

**Toolbox**
${toolbox}


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
row_2015 = df[df["Year"] == 2015]
row_2016 = df[df["Year"] == 2016]
games_2015 = row_2015["Vacation days"].values[0]
games_2016 = row_2016["Vacation days"].values[0]
rate_of_change = (games_2016 - games_2015) / (2016 - 2015)
print(rate_of_change)
```
**Tools**
```python
import pandas as pd
```


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
min_value = df["Number of laps"].min()
max_value = df["Number of laps"].max()
range_laps = max_value - min_value
print(range_laps)
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
