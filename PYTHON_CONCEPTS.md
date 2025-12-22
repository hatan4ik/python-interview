# 🐍 Python Concepts for Interviews (The "No Surprises" Guide)

This guide explains the "magic words" and concepts that appear in every Python interview but often confuse beginners.

---

## 1. `if __name__ == "__main__":` (The Gatekeeper)

**What is it?**
A line of code that asks: *"Am I being run directly by the user, or am I being imported by another script?"*

**Why do we need it?**
Imagine you have a script `math_tools.py` with a function `add(a, b)`.
If you write `print(add(2, 2))` at the bottom of `math_tools.py` and then run `import math_tools` in another file, that print statement will run immediately!

The `if __name__ == "__main__":` block prevents this. It ensures code only runs when you explicitly execute the file.

**Example:**
```python
def my_function():
    print("Function logic")

if __name__ == "__main__":
    # This only runs if you type 'python my_script.py'
    my_function()
```

---

## 2. Mutable vs. Immutable (The Trap)

**The Concept:**
Some data types can be changed after creation (Mutable). Others cannot (Immutable).

*   **Immutable (Safe):** Strings, Integers, Tuples `()`.
    *   If you change a string, Python actually makes a *new* string in memory.
*   **Mutable (Dangerous):** Lists `[]`, Dictionaries `{}`.
    *   If you pass a list to a function and the function changes it, the *original* list changes too!

**Interview Question:**
*"What happens if I pass a list to a function?"*
**Answer:** *"Lists are passed by reference (mutable). Modifications inside the function affect the original list."*

---

## 3. List Comprehensions (The Python Flex)

**The Concept:**
A shorthand way to create lists. It's considered "Pythonic" (the pro way).

**Old Way:**
```python
squares = []
for x in range(10):
    squares.append(x * x)
```

**Pro Way (List Comprehension):**
```python
squares = [x * x for x in range(10)]
```
*Read it as: "Give me x squared, for every x in the range."*

---

## 4. `args` and `kwargs` (The Magic Inputs)

**The Concept:**
Sometimes you don't know how many arguments a user will pass to your function.

*   `*args`: "Arguments". Captures extra variables into a **Tuple**.
*   `**kwargs`: "Keyword Arguments". Captures extra named variables into a **Dictionary**.

**Example:**
```python
def log_message(message, *args):
    print(message)
    # args might contain (1, 2, "error")
```

---

## 5. `with open(...)` (Context Managers)

**The Concept:**
Opening files is risky. If your script crashes before you close the file, you can corrupt data or run out of handles.

The `with` keyword creates a **Context Manager**. It guarantees the file is closed, even if an error occurs.

**Bad Way:**
```python
f = open("file.txt")
data = f.read()
f.close() # If read() fails, this never happens!
```

**Good Way:**
```python
with open("file.txt") as f:
    data = f.read()
# f.close() is called automatically here
```
