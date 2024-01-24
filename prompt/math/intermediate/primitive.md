Your task is to use tools, i.e., Python functions, to solve math questions.
Write a program solution to the question by decomposing it into multiple steps. Then specify the tools used in each step by importing from the toolbox. Make sure that all tools used in the solution are defined in the toolbox. Do not use any undefined functions.
You can use functions in math, scipy, sympy if they help.

**Toolbox**
${toolbox}


**Question**
Evaluate $|2\omega^2-4\omega-30|$ if $\omega=1-5i$.
**Solution**
```python
omega = 1 - 5j
expression = abs(2*omega**2 - 4*omega - 30)
print(expression)
```


**Question**
Find the number of ordered triples $(a,b,c)$ of integers with $1 \le a,$ $b,$ $c \le 100$ and
\[a^2 b + b^2 c + c^2 a = ab^2 + bc^2 + ca^2.\]
**Solution**
```python
count = 0
for a in range(1, 101):
    for b in range(1, 101):
        for c in range(1, 101):
            if a**2 * b + b**2 * c + c**2 * a == a * b**2 + b * c**2 + c * a**2:
                count += 1
print(count)
```


**Question**
${question}
**Solution**
