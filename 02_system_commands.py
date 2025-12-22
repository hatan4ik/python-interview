#!/usr/bin/env python3
"""
System Automation & Monitoring.

This module replaces fragile Bash scripts with robust Python logic.
It demonstrates:
1. subprocess.run for safe shell command execution.
2. pathlib for object-oriented filesystem traversal.
"""

import subprocess
from pathlib import Path

def check_disk_usage(mount_point: str = "/", threshold_percent: int = 80) -> None:
    """
    Checks the disk usage of a specific mount point and prints alerts.

    Args:
        mount_point (str): The filesystem path to check (default: "/").
        threshold_percent (int): The percentage usage that triggers an alert.
    
    Note:
        Uses 'df -h' internally. This is compatible with Linux and macOS.
    """
    print("--- Checking Disk Usage ---")
    
    # We pass a LIST of arguments to avoid Shell Injection vulnerabilities.
    command = ["df", "-h", mount_point]
    
    try:
        # capture_output=True allows us to parse stdout.
        # check=True raises an exception if the command fails (exit code != 0).
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Output parsing logic
        output_lines = result.stdout.strip().split('\n')
        data_line = output_lines[1] 
        parts = data_line.split()
        
        # Index 4 is standard for 'Use%' or 'Capacity' on most Unix systems
        use_percent_str = parts[4].replace('%', '')
        use_percent = int(use_percent_str)
        
        print(f"Current Disk Usage: {use_percent}%")
        
        if use_percent > threshold_percent:
            print(f"ALERT: Disk usage is critical! (> {threshold_percent}%)")
        else:
            print("Disk usage is within normal limits.")
            
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def find_large_files(start_path: Path, size_mb: int = 100) -> None:
    """
    Recursively scans a directory for files larger than a specific size.

    Args:
        start_path (Path): The root directory to start scanning.
        size_mb (int): The size threshold in Megabytes.
    """
    print(f"\n--- Scanning for files larger than {size_mb}MB in {start_path} ---")
    
    limit_bytes = size_mb * 1024 * 1024
    
    try:
        # .rglob('*') is a generator that recursively yields all files.
        # It is memory efficient even for large directory trees.
        for file_path in start_path.rglob('*'):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    if size > limit_bytes:
                        size_in_mb = size / (1024 * 1024)
                        print(f"Large file found: {file_path} ({size_in_mb:.2f} MB)")
                except OSError:
                    # PermissionDenied or FileNotFoundError during scan
                    continue
    except Exception as e:
        print(f"Error scanning directory: {e}")

if __name__ == "__main__":
    check_disk_usage(threshold_percent=2) # Low threshold for demo purposes
    find_large_files(Path("."))
