import tracemalloc

tracemalloc.start(10)
snap_1 = tracemalloc.take_snapshot()

bunch_of_numbers = [x*x for x in range(10000)]

snap_2 = tracemalloc.take_snapshot()

inventory = snap_2.compare_to(snap_1, "lineno")
for item in inventory[:2]:
    print(item)

