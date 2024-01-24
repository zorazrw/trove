Your task is to generate and use tools, i.e., Python functions, to answer question about tables.
Write a program solution to the question by decomposing it into multiple steps. Then specify the tools used in each step by importing from the toolbox. Make sure that all tools used in the solution are defined in the toolbox. Do not use any undefined functions.
You can use functions in numpy, pandas if they help. Each table is presented in markdown format, you can transform tables into pandas DataFrame objects. Each table is stored in a json file, you can transform tables into pandas DataFrame objects.

**Toolbox**
${toolbox}


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
women_percent = df.loc[left_index, top_index_women]
top_index_men = ('men', 'university degree only')
men_percent = df.loc[left_index, top_index_men]
percent_higher = women_percent - men_percent
print(percent_higher)
```
**Tools**
```python
from toolbox import parse_table
```


**Question**
${question}
**Table**
${table}
**Solution**

