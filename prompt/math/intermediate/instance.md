Your task is to write the solution with high-level tools, i.e., Python functions, to solve math questions.
Think about the potential program solution for this example, you can create high-level functions, that could be used to solve this example. For example, if the solution involves multiple actions that are always used together, it is more efficient to create and use the tool.

**Toolbox**
${toolbox}


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


**Question**
${question}
**Solution**
