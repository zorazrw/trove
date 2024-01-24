You task is to write Python program solutions to the given math problems.
You should also create Python functions that can be used by your solution, if you believe the function can be reused to solve other questions.


## Example
**Question**
The remainder when $kx^4+9x^3+kx^2+32x-11$ is divided by $x + 5$ is $4$.  Find $k.$

**Solution**
```python
k, x = symbols('k x')
eq = k*x**4 + 9*x**3 + k*x**2 + 32*x - 11
remainder = sympy.rem(eq, x + 5)
k_value = solve(remainder - 4, k)
print(k_value[0])
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
