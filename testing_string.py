import tracemalloc
tracemalloc.start(10)

import numpy as np


snap_1 = tracemalloc.take_snapshot()

list_of_strings = []
for i in range(10000000):
    list_of_strings.append(f"{i}")


arr = np.empty(10000000, dtype=object)
for i in range(10000000):
    arr[i] = f"{i}"

snap_2 = tracemalloc.take_snapshot()

inventory = snap_2.compare_to(snap_1, "lineno")
for item in inventory[:4]:
    print(item)



