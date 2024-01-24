You task is to write Python program solutions to the given math problems.
The toolbox section lists all the available functions that can be used in your solution.


## Example
**Question**
In right triangle $ABC$ with $\angle B = 90^\circ$, we have $\sin A = 2\cos A$.  What is $\tan A$?

**Toolbox**
```python
# Import math library
import math
```
```python
# import symbols and solving functions
from sympy import symbols, solve
```

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
from sympy import symbols, solve
```


## Example
**Question**
${question}

**Toolbox**
${toolbox}

**Solution**
