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

res_df["gain_through_cat"] = (res_df["mem_cat"] - res_df["mem_str"]) / res_df["mem_str"]

res_pv = res_df.pivot(index='nr_strings', columns='nr_reps')['gain_through_cat'].round(2)
print(res_pv.to_markdown())
