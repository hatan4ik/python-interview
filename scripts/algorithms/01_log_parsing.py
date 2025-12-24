#!/usr/bin/env python3
"""
Log Parsing & Analysis Module.

This script demonstrates high-performance log parsing techniques suitable for
DevOps interviews. It covers:
1. Regex pattern compilation for efficiency.
2. Generator-like line processing.
3. Memory-efficient counting using collections.Counter.
"""

import re
from collections import Counter
from pathlib import Path
from typing import Pattern

# ==========================================
# SETUP: Create dummy log file
# ==========================================
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

def ensure_sample_log(log_file: Path) -> None:
    """
    Creates a sample log file if it does not already exist.
    """
    if log_file.exists():
        return
    log_file.write_text(LOG_CONTENT.strip(), encoding="utf-8")


def parse_logs(log_file: Path) -> None:
    """
    Parses a web server log file to extract traffic metrics.

    Args:
        log_file (Path): The path to the log file to read.

    Returns:
        None: Prints analysis results directly to stdout.

    Raises:
        FileNotFoundError: If the specified log_file does not exist.
    """
    print(f"--- Analyzing {log_file} ---")
    
    ip_counter: Counter[str] = Counter()
    server_errors: int = 0
    
    # Compile Regex once outside the loop for O(1) reuse.
    # Group 1: IP Address (\d+...)
    # Group 2: Status Code (\d{3})
    log_pattern: Pattern[str] = re.compile(r'(\d+\.\d+\.\d+\.\d+).*?"\w+ .*? HTTP/1.1" (\d{3})')

    try:
        # Open with encoding explicitly specified for cross-platform safety
        with log_file.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                # Walrus Operator (:=) checks match and assigns it in one step.
                if match := log_pattern.search(line):
                    ip = match.group(1)
                    status_code = match.group(2)
                    
                    if status_code == '500':
                        server_errors += 1
                    
                    ip_counter[ip] += 1
                    
    except FileNotFoundError:
        print(f"Error: The file {log_file} was not found.")
        return

    print(f"Total 500 Errors found: {server_errors}")
    
    print("\nRequest Counts per IP:")
    for ip, count in ip_counter.items():
        print(f"{ip}: {count}")
        
    print("\nTop 3 Frequent IPs:")
    for ip, count in ip_counter.most_common(3):
        print(f"  {ip}: {count} requests")

if __name__ == "__main__":
    ensure_sample_log(FILENAME)
    parse_logs(FILENAME)
