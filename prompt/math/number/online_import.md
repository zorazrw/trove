You task is to write Python program solutions to the given math problems.
The toolbox section lists all the available functions that can be used in your solution.


## Example
**Question**
To determine whether a number $\textit{N}$ is prime, we must test for divisibility by every prime less than or equal to the square root of $\textit{N}$. How many primes must we test to determine whether $2003$ is prime?

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
N = 2003
sqrt_N = math.sqrt(N)
primes = [2]
for num in range(3, int(sqrt_N)+1, 2):
    is_prime = True
    for prime in primes:
        if num % prime == 0:
            is_prime = False
            break
    if is_prime:
        primes.append(num)
num_primes = len(primes)
print(num_primes)
```
**Tools**
```python
import math
```


## Example
**Question**
${question}

**Toolbox**
${toolbox}

**Solution**
