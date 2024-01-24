You task is to write Python program solutions to the given math problems.


## Example
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
**Tools**
```python
```


## Example
**Question**
${question}

**Solution**
