Your task is to write the solution with high-level tools, i.e., Python functions, to solve math questions.
Think about the potential program solution for this example, you can create high-level functions, that could be used to solve this example. For example, if the solution involves multiple actions that are always used together, it is more efficient to create and use the tool.

**Toolbox**
${toolbox}


**Question**
Points $A, B, C$ and $D$ have these coordinates: $A(3,2)$, $B(3,-2)$, $C(-3,-2)$ and $D(-3,0)$. What is the area of quadrilateral $ABCD$?
**Solution**
```python
points = np.array([[3, 2], [3, -2], [-3, -2], [-3, 0]])
area = 0.5 * abs(np.dot(points[:, 0], np.roll(points[:, 1], 1)) - np.dot(points[:, 1], np.roll(points[:, 0], 1)))
print(area)
```
**Tools**
```python
import numpy as np
```


**Question**
In right triangle $ABC$ with $\angle B = 90^\circ$, we have $\sin A = 2\cos A$.  What is $\tan A$?
**Solution**
```python
A = symbols('A')
eq = sympy.sin(A) - 2*sympy.cos(A)
solution = solve(eq, A)
A_value = solution[0]
tan_A = sympy.tan(A_value)
print(tan_A)
```
**Tools**
```python
import sympy
from sympy import symbols, solve
```


**Question**
${question}
**Solution**
