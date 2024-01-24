You task is to write Python program solutions to the given math problems.
You should also create Python functions that can be used by your solution, if you believe the function can be reused to solve other questions.


## Example
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


## Example
**Question**
${question}

**Solution**
