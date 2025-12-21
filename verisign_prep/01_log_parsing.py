import re
from collections import Counter
from datetime import datetime

# ==========================================
# SCENARIO:
# You have a server log file. 
# 1. Parse the file to find all 500 (Server Error) status codes.
# 2. Count the number of requests per IP address.
# 3. Print the top 3 most frequent IPs.
# ==========================================

# 1. SETUP: Create a dummy log file for this exercise
log_content = """
192.168.1.1 - - [21/Dec/2025:10:00:01 +0000] "GET /home HTTP/1.1" 200 1024
192.168.1.2 - - [21/Dec/2025:10:00:02 +0000] "GET /app HTTP/1.1" 500 512
10.0.0.5 - - [21/Dec/2025:10:00:03 +0000] "POST /login HTTP/1.1" 200 4096
192.168.1.1 - - [21/Dec/2025:10:00:04 +0000] "GET /dashboard HTTP/1.1" 200 2048
192.168.1.2 - - [21/Dec/2025:10:00:05 +0000] "GET /app HTTP/1.1" 500 512
10.0.0.5 - - [21/Dec/2025:10:00:06 +0000] "POST /upload HTTP/1.1" 201 8192
192.168.1.2 - - [21/Dec/2025:10:00:07 +0000] "GET /app HTTP/1.1" 500 512
192.168.1.100 - - [21/Dec/2025:10:00:08 +0000] "GET /config HTTP/1.1" 404 128
"""

filename = "server.log"
with open(filename, "w") as f:
    f.write(log_content.strip())

# ==========================================
# SOLUTION
# ==========================================

def parse_logs(log_file):
    print(f"--- Analyzing {log_file} ---")
    
    # Counter is a specialized dictionary designed for counting hashable objects.
    # It's much cleaner than: if ip in dict: dict[ip] += 1 else: dict[ip] = 1
    ip_counter = Counter()
    server_errors = 0
    
    # Regex Explanation:
    # (\d+\.\d+\.\d+\.\d+)  -> Capture Group 1: Matches an IP address (digits.digits...)
    # .*?                   -> Non-greedy match for anything in between
    # "\w+ .*? HTTP/1.1"    -> Matches the method and path
    # \s+                   -> Whitespace
    # (\d{3})               -> Capture Group 2: The Status Code (3 digits)
    log_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+).*?"\w+ .*? HTTP/1.1" (\d{3})')

    try:
        # 'with' statement ensures file is closed automatically (Context Manager)
        with open(log_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line: continue
                
                # Approach 1: String Splitting (Simpler, faster for structured logs)
                # parts = line.split()
                # ip = parts[0]
                # status = parts[-2]
                
                # Approach 2: Regex (More robust, good for messy logs)
                match = log_pattern.search(line)
                if match:
                    ip = match.group(1)
                    status_code = match.group(2)
                    
                    # Task 1: Count 500 errors
                    if status_code == '500':
                        server_errors += 1
                    
                    # Task 2: Count requests per IP
                    ip_counter[ip] += 1
                    
    except FileNotFoundError:
        print("Error: File not found.")
        return

    print(f"Total 500 Errors found: {server_errors}")
    
    print("\nRequest Counts per IP:")
    for ip, count in ip_counter.items():
        print(f"{ip}: {count}")
        
    # Task 3: Top 3 IPs
    print("\nTop 3 Frequent IPs:")
    # Counter.most_common(n) returns a list of (element, count) tuples
    for ip, count in ip_counter.most_common(3):
        print(f"  {ip}: {count} requests")

if __name__ == "__main__":
    parse_logs(filename)
