#!/usr/bin/env python3
import re
from collections import Counter
from pathlib import Path
from typing import Pattern

# ==========================================
# SCENARIO:
# Parse logs using Modern Python (3.10+) standards.
# Key Modern Features:
# 1. 'pathlib' for file handling (replaces 'os' and 'open' boilerplate)
# 2. Type Hinting (str, Path, etc.)
# 3. Walrus Operator (:=) for concise conditional assignments
# ==========================================

# 1. SETUP: Create dummy log file using pathlib
LOG_CONTENT = """
192.168.1.1 - - [21/Dec/2025:10:00:01 +0000] "GET /home HTTP/1.1" 200 1024
192.168.1.2 - - [21/Dec/2025:10:00:02 +0000] "GET /app HTTP/1.1" 500 512
10.0.0.5 - - [21/Dec/2025:10:00:03 +0000] "POST /login HTTP/1.1" 200 4096
192.168.1.1 - - [21/Dec/2025:10:00:04 +0000] "GET /dashboard HTTP/1.1" 200 2048
192.168.1.2 - - [21/Dec/2025:10:00:05 +0000] "GET /app HTTP/1.1" 500 512
10.0.0.5 - - [21/Dec/2025:10:00:06 +0000] "POST /upload HTTP/1.1" 201 8192
192.168.1.2 - - [21/Dec/2025:10:00:07 +0000] "GET /app HTTP/1.1" 500 512
192.168.1.100 - - [21/Dec/2025:10:00:08 +0000] "GET /config HTTP/1.1" 404 128
"""

FILENAME = Path("server.log")
FILENAME.write_text(LOG_CONTENT.strip(), encoding="utf-8")

# ==========================================
# SOLUTION
# ==========================================

def parse_logs(log_file: Path) -> None:
    print(f"--- Analyzing {log_file} ---")
    
    ip_counter: Counter[str] = Counter()
    server_errors: int = 0
    
    # Pre-compiling regex is a standard optimization
    log_pattern: Pattern[str] = re.compile(r'(\d+\.\d+\.\d+\.\d+).*?"\w+ .*? HTTP/1.1" (\d{3})')

    try:
        # pathlib.open() is cleaner
        with log_file.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                # OPTIMIZATION: Walrus Operator (:=)
                # Assigns 'match' AND checks if it is truthy in one line.
                # Available since Python 3.8, standard in 3.10+ styles.
                if match := log_pattern.search(line):
                    ip = match.group(1)
                    status_code = match.group(2)
                    
                    if status_code == '500':
                        server_errors += 1
                    
                    ip_counter[ip] += 1
                    
    except FileNotFoundError:
        print("Error: File not found.")
        return

    print(f"Total 500 Errors found: {server_errors}")
    
    print("\nRequest Counts per IP:")
    for ip, count in ip_counter.items():
        print(f"{ip}: {count}")
        
    print("\nTop 3 Frequent IPs:")
    for ip, count in ip_counter.most_common(3):
        print(f"  {ip}: {count} requests")

if __name__ == "__main__":
    parse_logs(FILENAME)