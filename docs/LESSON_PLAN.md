# Verisign DevOps Python Interview Prep

Based on common DevOps interview patterns and Verisign's specific focus on infrastructure, security, and reliability, here is a targeted study plan.

## Core Pillars

1.  **Text Processing & Log Analysis**: This is the #1 DevOps coding task. You will likely be given a log file and asked to extract specific metrics (e.g., "Count 500 errors by IP address").
2.  **System Interaction**: Automating shell tasks using Python (`subprocess`, `os`).
3.  **API Interaction**: Querying REST endpoints, parsing JSON, and checking service health.
4.  **Data Structures**: Efficiently using Lists, Dictionaries (Hash Maps), and Sets.

## Top Concepts to Master

*   **File I/O**: `with open('file.log', 'r') as f:`
*   **String Manipulation**: `.split()`, `.strip()`, `f-strings`.
*   **Regex (`re` module)**: Extracting IPs, dates, or error codes.
*   **Collections**: `Counter` from `collections` is a cheat code for counting things.
*   **Subprocess**: `subprocess.run(['ls', '-l'], capture_output=True, text=True)`
*   **Error Handling**: `try/except` blocks to ensure scripts don't crash on bad input.

## The Strategy

We have prepared 5 executable Python examples in this directory. Run them, read the code, and understand the logic.

1.  `scripts/01_log_parsing.py`: The "FizzBuzz" of DevOps. Essential.
2.  `scripts/02_system_commands.py`: How to replace Bash scripts with Python.
3.  `scripts/03_api_checks.py`: Monitoring and JSON handling.
4.  **Review the code comments**: They contain the "why" and "how" explanations you should give during the interview.
