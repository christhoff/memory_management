# Pandas dtypes: To category or not to category
Starting out programming in Python is easy. Python is designed with user-friendliness in mind.
You can quickly write programs without the need to think about data types or memory management.
But once you scale your code to production-like settings with bigger workloads and complexity, 
you need to step up your Python game.

When it comes to data analysis Pythons pandas library offers a lot of optimization potential out of the box, but relying on 
default settings is risky.
One case in hand are dtypes, the data types of your columns (like float or integer). For the most part, pandas uses NumPy arrays and dtypes for 
individual columns of a DataFrame and extends those at a few places.

The dtype describes how the bytes in the fixed-size block of memory corresponding to an underlying array item should be interpreted. 
It describes things like the type of data, the size of the data or the byte order of the data.

Pandas default dtypes are not always memory efficient. This is particularly true for strings.
Pandas official documentations recommends casting text data columns with relatively few unique values (“low-cardinality” data) as type Categorical.
Now you might ask yourself how low is low enough to profit from recasting?

The answer is analytical in nature, but 20 minutes of coding can spare you 5 minutes of thinking, so I wrote a quick simulation on memory reduction through recasting:

```python

import pandas as pd
from tabulate import tabulate

number_of_strings = [10**5, 10**6, 10**7]
number_of_repetitions = [1, 2, 10, ]
results = []

for strings in number_of_strings:
    for reps in number_of_repetitions:
        df = pd.DataFrame({"string_name": [f"string_abc_{i}" for i in range(strings)]*reps}, dtype="string")
        memory_str = df.memory_usage(deep=True)["string_name"]
        df = df.astype("category")
        memory_cat = df.memory_usage(deep=True)["string_name"]
        results.append([strings, reps, memory_str, memory_cat])

res_df = pd.DataFrame(results, columns=["nr_strings", "nr_reps", "mem_str", "mem_cat"])

res_df["gain_through_cat"] = (res_df["mem_cat"] - res_df["mem_str"]) / res_df["mem_str"].round()

```
Two parameters drive our investigation. How many keys do we have in general and how often do they repeat themselves.
Here is the memory gain from using category in percent:

```python
res_pv = res_df.pivot(index='nr_strings', columns='nr_reps')['gain_through_cat'].round(2)
print(res_pv.to_markdown())
```

|   nr_strings |    1 |     2 |    10 |
|-------------:|-----:|------:|------:|
|       100000 | 0.34 | -0.3  | -0.82 |
|      1000000 | 0.51 | -0.22 | -0.8  |
|     10000000 | 0.41 | -0.27 | -0.81 |

If all keys are unique feel free to stick with the default dtype, but once you expect your strings to repeat themselves once, start using categorical dtypes.
On average you will save 30% of memory. Once your strings show up 10 times or more, memory gain is up to 80%.



