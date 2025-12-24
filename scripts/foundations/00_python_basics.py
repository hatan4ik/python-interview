#!/usr/bin/env python3
"""
Level 0: Python Basics
This file explains the absolute fundamentals: Variables, Functions (def), and Logic.
"""

# ==========================================
# 1. WHAT IS 'def'?
# ==========================================
# 'def' stands for DEFINE. We use it to create a "Function".
# A function is a reusable block of code.

def greet_user(name):
    """
    This function takes one input (name) and prints a greeting.
    """
    # Indentation (4 spaces) tells Python this code belongs to the function.
    print(f"Hello, {name}!") 
    print("Welcome to Python.")

# ==========================================
# 2. RETURNING VALUES
# ==========================================
# Sometimes functions don't just print; they give back (return) an answer.

def add_numbers(a, b):
    result = a + b
    return result  # Sends the value back to whoever called it

# ==========================================
# 6. THE "MAIN" GUARD (if __name__ == "__main__":)
# ==========================================
# You will see this in almost every professional Python script.
# It means: "If you run this file directly, do this. If you import it, do nothing."

def run_demo():
    # The code above DOES NOT RUN yet. It just "defines" the tool.
    # We have to "call" it to use it.
    print("--- Running Function ---")
    greet_user("Nathanels")  # formatting: calls the function with "Nathanels"
    greet_user("Interviewer") # calls it again with "Interviewer"

    print("\n--- Return Values ---")
    sum_value = add_numbers(10, 5) # sum_value becomes 15
    print(f"The sum is: {sum_value}")

    # ==========================================
    # 3. VARIABLES (Data Types)
    # ==========================================
    # Variables are like boxes with labels.
    print("\n--- Variables ---")
    my_name = "Alice"       # String (text)
    my_age = 30             # Integer (whole number)
    is_hired = True         # Boolean (True/False)
    hourly_rate = 55.5      # Float (decimal)

    print(f"Name: {my_name}, Hired: {is_hired}")

    # ==========================================
    # 4. LOGIC (If / Else)
    # ==========================================
    # Making decisions based on data.
    print("\n--- Logic ---")
    score = 85

    if score >= 90:
        print("Grade: A")
    elif score >= 80:
        print("Grade: B") # This will print
    else:
        print("Grade: C")

    # ==========================================
    # 5. LOOPS (Repeat stuff)
    # ==========================================
    # Do the same thing multiple times.
    print("\n--- Loops ---")
    # "range(3)" creates a sequence: 0, 1, 2
    for i in range(3):
        print(f"Counting: {i}")

    print("\n--- Inside Main Function ---")
    print("This code runs only when you execute the file directly.")

def main():
    run_demo()

    print("\n--- Inside Main Function ---")
    print("This code runs only when you execute the file directly.")

# "if __name__ == '__main__':" is the Gatekeeper.
if __name__ == "__main__":
    main()
    # Why use it?
    # 1. Organization: It keeps your global scope clean.
    # 2. Imports: Allows other scripts to import your functions WITHOUT running them immediately.
