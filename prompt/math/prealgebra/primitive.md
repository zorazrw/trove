Your task is to use tools, i.e., Python functions, to solve math questions.
Write a program solution to the question by decomposing it into multiple steps. Then specify the tools used in each step by importing from the toolbox. Make sure that all tools used in the solution are defined in the toolbox. Do not use any undefined functions.
You can use functions in math, scipy, sympy if they help.

**Toolbox**
${toolbox}


**Question**
A math club is having a bake sale as a fundraiser to raise money for an upcoming trip. They sell $54$ cookies at three for $\$1$, and $20$ cupcakes at $\$2$ each, and $35$ brownies at $\$1$ each. If it cost the math club $\$15$ to bake these items, what was their profit?
**Solution**
```python
cookies_sold, cupcakes_sold, brownies_sold = 54, 20, 35
cookies_price, cupcakes_price, brownies_price = 1/3, 2, 1
total_cost = 15
revenue = (cookies_sold * cookies_price) + (cupcakes_sold * cupcakes_price) + (brownies_sold * brownies_price)
profit = revenue - total_cost
print(profit)
```


**Question**
${question}
**Solution**
