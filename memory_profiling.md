## Memorize your memory references with tracemalloc

Starting out programming in Python is a charm. Python is designed with user friendlyness in mind.
You can quickly write programs without the need to think about data types or memory management.
But once you scale your code to production-like settings with bigger workloads and complexity, 
you need to step up your Python game. One trick up your sleeves might be tracemalloc, a tool to capture rampant memory objects.

Pythons default implementation, CPython, uses reference counting for memory management.
Once you remove all references to an object, the object is cleared from memory for you. 
But if you decide to keep the references alive, don't be surprised if objects stay around and start hunting you.

### Python Memory management: Reference counting

To get started with memory management in Python, think name, reference and object.
The name is just a label for your object. And you can have multiple names referencing one object.
Look at the following example. Here we have two names, name_1 and name_2, that are both referencing the same object.
You can see this by calling the id function on them, displaying the memory address of the object.
The reference count just counts the number of references you have to an object. In this instance two.

```python
>>> name_1 = 100
>>> name_2 = 100

id(name_1)
139878446196176
id(name_2)
139878446196176
```

The reference count is part of an object, and every time you let a name reference the object you increment the count, everytime you remove a reference
you decrement the count. One way to remove a reference is to use the del keyword on the name, like del name_1.
Once the reference count is zero, the object will be removed from memory for you.

The most important way to remove references is by changing scopes, for instance by calling and exiting functions:

```python
>>> def print_me():
...     name_1 = "Peace"
...     print(name_1)

>>> print_me()
Peace
```

If you invoke the print_me function, you will create a string object and reference it by the name name_1.
The reference count is up by one. Once the function is excited, the reference is out of scope and the counter decrements to zero.
The object will be released from memory.

### tracemalloc

The tracemalloc module allows you to do memory inventory management.
The idea is simple, take two snapshots from memory and see what and where it has changed.

In the code snippet below we create a bunch of numbers and tracemalloc displays the line number of object creation, the number of objects crated, their total as well as their
average size. Can you guess why the number of created objects is not equal to 1000?

```python
# example_tracemalloc.py
import tracemalloc

tracemalloc.start(10)
snap_1 = tracemalloc.take_snapshot()

bunch_of_numbers = [x*x for x in range(10000)]

snap_2 = tracemalloc.take_snapshot()

inventory = snap_2.compare_to(snap_1, "lineno")
for item in inventory[:2]:
    print(item)
```

```python
example_tracemalloc.py:6: size=356 KiB (+356 KiB), count=9984 (+9984), average=37 B
example_tracemalloc.py:4: size=576 B (+576 B), count=1 (+1), average=576 B
```

### Identify useless references
Without getting rid of references memory objects start to pile. Below you find a simplified example. We create some input
data and then apply two operations to it.
How much of the data will stay in memory during execution? The regular calls to get_traced_memory indicate
that you keep adding data to memory. What would happen instead if you would apply the del keyword?

```python
#example_unused_memory.py
import tracemalloc

def print_current_peak_mem():
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current}. Peak memory usage: {peak}")


tracemalloc.start(10)
snap_1 = tracemalloc.take_snapshot()

input_numbers = [x*x for x in range(10000)]
print_current_peak_mem()

operation_1 = [x/2 for x in input_numbers]
print_current_peak_mem()

#del input_numbers

operation_2 = [x/2 for x in operation_1]
print_current_peak_mem()

snap_2 = tracemalloc.take_snapshot()

inventory = snap_2.compare_to(snap_1, "lineno")
for stat in inventory[:3]:
    print(stat)
```
```python
Current memory usage: 364820. Peak memory usage: 365032
Current memory usage: 690310. Peak memory usage: 690494
Current memory usage: 1015862. Peak memory usage: 1016046
example_unused_memory.py:11: size=356 KiB (+356 KiB), count=9984 (+9984), average=37 B
example_unused_memory.py:19: size=318 KiB (+318 KiB), count=10002 (+10002), average=33 B
example_unused_memory.py:14: size=318 KiB (+318 KiB), count=9998 (+9998), average=33 B
```

### Where to go from here?
This blog post borrows heavily from three great sources, which you can consult for a more detailed intro:
- Main motivation and further resources by Itamar Turner-Trauring (https://pythonspeed.com/)
- Great video intro on memory management by Nina Zakharenko, PyCon 2016
- Item 81 of Brett Slatkins Effective Python
