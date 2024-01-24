Your task is to write the solution with high-level tools, i.e., Python functions, to solve math questions.
Think about the potential program solution for this example, you can create high-level functions, that could be used to solve this example. For example, if the solution involves multiple actions that are always used together, it is more efficient to create and use the tool.

**Toolbox**
${toolbox}


**Question**
Simplify $\sqrt{64^3}$.
**Solution**
```python
result = math.sqrt(64**3)
print(result)
```
**Tools**
```python
import math
```


**Question**
Bill walks $\frac{1}{2}$ mile south, then $\frac{3}{4}$ mile east, and finally $\frac{1}{2}$ mile south. How many miles is he, in a direct line, from his starting point?  Express your answer as a decimal to the nearest hundredth.
**Solution**
```python
distance = math.sqrt((0.5 + 0.5)**2 + (0.75)**2)
print(f"{distance:.2f}")
```
**Tools**
```python
import math
```


**Question**
${question}
**Solution**
