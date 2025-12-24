# DevOps Interview Cheat Sheet: Python vs. Bash

This guide contrasts the two most critical languages for a DevOps Engineer. Knowing when to use which is often the difference between a "Junior" and "Senior" grade in an interview.

## 1. Log Parsing & Text Processing
**Scenario**: "Find the top 3 IP addresses in a log file."

### 🐍 Python
**Pros**: Readable, handles complex logic/regex easily, easier to test.
```python
from collections import Counter
import re

# Read entire file (for small files)
content = open('server.log').read()
ips = re.findall(r'\d+\.\d+\.\d+\.\d+', content)

# Count and get top 3
print(Counter(ips).most_common(3))
```

### 🐚 Bash
**Pros**: Extremely fast to write (one-liner), zero dependencies, native to the shell.
```bash
# 1. awk prints IP (1st column)
# 2. sort groups them
# 3. uniq -c counts them
# 4. sort -nr sorts by count (descending)
# 5. head gets top 3
awk '{print $1}' server.log | sort | uniq -c | sort -nr | head -3
```

---

## 2. API Health Checks
**Scenario**: "Check if a service is up (200 OK)."

### 🐍 Python
**Pros**: Handles JSON responses naturally, better exception handling.
```python
import urllib.request

try:
    resp = urllib.request.urlopen("https://httpbin.org/get")
    print(f"Status: {resp.getcode()}")
except Exception as e:
    print(f"Error: {e}")
```

### 🐚 Bash
**Pros**: Quick, great for simple "up/down" checks in CI pipelines.
```bash
# -s: Silent
# -o /dev/null: Ignore body
# -w: Write status code
curl -s -o /dev/null -w "%{http_code}" https://httpbin.org/get
```

---

## 3. System Resources (Disk Usage)
**Scenario**: "Alert if disk usage > 80%."

### 🐍 Python
**Pros**: Cross-platform (Windows/Linux compatibility), returns numeric types directly.
```python
import shutil

# shutil.disk_usage returns a named tuple (total, used, free)
total, used, free = shutil.disk_usage("/")
percent = (used / total) * 100

if percent > 80:
    print("Alert!")
```

### 🐚 Bash
**Pros**: Standard on all Unix systems, no imports needed.
```bash
# Use awk to strip the '%' sign
USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')

if [ "$USAGE" -gt 80 ]; then
    echo "Alert!"
fi
```

---

## 4. Find Common Elements (Intersection)
**Scenario**: "Which servers are in both list A and list B?"

### 🐍 Python
**Pros**: O(1) lookups with Sets, highly efficient for data.
```python
list_a = ["server1", "server2"]
list_b = ["server2", "server3"]

# Set Intersection
common = set(list_a) & set(list_b)
```

### 🐚 Bash
**Pros**: Good for file-based processing using streams.
```bash
# 'comm' requires sorted inputs
# -12: Suppress lines unique to file 1 and 2 (show only common)
comm -12 <(sort list_a.txt) <(sort list_b.txt)
```

---

## 5. Loops & Logic (FizzBuzz)
**Scenario**: "Print 1 to 10."

### 🐍 Python
```python
# 'range' is exclusive at the top end
for i in range(1, 11):
    print(i)
```

### 🐚 Bash
```bash
# 'seq' generates sequences
seq 1 10
# OR C-style for loop
for ((i=1;i<=10;i++)); do echo $i; done
```

---

## ⚡ The "Senior Engineer" Answer
**Interviewer**: "Which one would you use?"

**You**:
> "It depends on the **complexity** and **lifecycle** of the task.
>
> *   **Use Bash** for simple, one-off tasks, data piping, or CI/CD wrapper scripts where dependencies are a pain. It's the 'glue' code.
> *   **Use Python** for complex logic (loops/conditionals), parsing structured data (JSON/YAML), or anything that needs to be maintained, tested, or run on Windows.
>
> **Rule of Thumb**: If the Bash script is longer than 50 lines, rewrite it in Python."
