Your task is to use tools, i.e., Python functions, to solve math questions.
Write a program solution to the question by decomposing it into multiple steps. Then specify the tools used in each step by importing from the toolbox. Make sure that all tools used in the solution are defined in the toolbox. Do not use any undefined functions.
You can use functions in math, scipy, sympy if they help.

**Toolbox**
${toolbox}


**Question**
A company makes a six-sided hollow aluminum container in the shape of a rectangular prism as shown. The container is $10^{''}$ by $10^{''}$ by $12^{''}$. Aluminum costs $\$0.05$ per square inch. What is the cost, in dollars, of the aluminum used to make one container?

[asy]

import three;

draw((0,0,0)--(1,0,0)--(1,1,0)--(0,1,0)--(0,0,0)--cycle,linewidth(1));

draw((1,0,0)--(1,0,-1)--(1,1,-1)--(1,1,0)--(1,0,0)--cycle,linewidth(1));

draw((0,1,0)--(1,1,0)--(1,1,-1)--(0,1,-1)--(0,1,0)--cycle,linewidth(1));

label("$12^{''}$",(1,0,-.5),W);

label("$10^{''}$",(.5,0,0),N);

label("$10^{''}$",(0,.5,0),N);

[/asy]
**Solution**
```python
length, width, height = 10, 10, 12
surface_area = 2 * (length * width + length * height + width * height)
cost = surface_area * 0.05
print(cost)
```


**Question**
${question}
**Solution**
