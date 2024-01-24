You task is to write Python program solutions to the given math problems.
You should also create Python functions that can be used by your solution, if you believe the function can be reused to solve other questions.


## Example
**Question**
What is the remainder when $2^3 \cdot 4^5 \cdot 6^7 \cdot 8^9$ is divided by 13?

**Solution**
```python
numbers = [2**3, 4**5, 6**7, 8**9]
product = np.prod(numbers)
remainder = product % 13
print(remainder)
```
**Tools**
```python
import numpy as np
```


## Example
**Question**
${question}

**Solution**
