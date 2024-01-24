You task is to write Python program solutions to the given math problems.
The toolbox section lists all the available functions that can be used in your solution.


## Example
**Question**
If $3p+4q=8$ and $4p+3q=13$, what is $q$ equal to?

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
p, q = symbols('p q')
eq1 = 3*p + 4*q - 8
eq2 = 4*p + 3*q - 13
solution = solve((eq1, eq2), (p, q))
q_value = solution[q]
print(q_value)
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
