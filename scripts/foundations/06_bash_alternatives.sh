#!/bin/bash

# ==========================================
# SCENARIO:
# The "Old School" DevOps approach.
# These are the precise commands to achieve the Python results 
# using native Unix tools (awk, sed, grep, curl, find).
# ==========================================

echo "========================================"
echo "1. LOG PARSING (Python vs Awk/Sort/Uniq)"
echo "========================================"
# Python: Counter() -> Bash: sort | uniq -c | sort -nr
# 1. awk '{print $1}': Extract first column (IP)
# 2. sort: Group them so uniq can work
# 3. uniq -c: Count occurrences
# 4. sort -nr: Sort Numerically, Reverse (descending)
# 5. head -3: Top 3
echo "Top 3 IPs from server.log:"
awk '{print $1}' server.log | sort | uniq -c | sort -nr | head -3

echo ""
echo "Count of 500 Errors:"
grep " 500 " server.log | wc -l


echo -e "\n========================================"
echo "2. SYSTEM COMMANDS (Python vs df/find)"
echo "========================================"
# Disk Usage
# NR==2: Select 2nd line (skip header)
# print $5: Print 5th column (Percentage)
# tr -d '%': Delete the percentage sign
USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
echo "Current Disk Usage: ${USAGE}%"

if [ "$USAGE" -gt 80 ]; then
    echo "ALERT: Disk Critical"
else
    echo "Disk OK"
fi

# Find Large Files (>100MB)
echo "Scanning for large files (ignoring errors)..."
find . -type f -size +100M -print 2>/dev/null || echo "No large files found."


echo -e "\n========================================"
echo "3. API CHECKS (Python vs curl/jq)"
echo "========================================"
# -s: Silent (no progress bar)
# -o /dev/null: Throw away body
# -w "%{http_code}": Write only the status code
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://httpbin.org/get)

if [ "$STATUS" -eq 200 ]; then
    echo "Service is UP (Status: $STATUS)"
    
    # Optional: Parse JSON if 'jq' is installed
    if command -v jq &> /dev/null;
    then
        echo "Parsed URL:"
        curl -s https://httpbin.org/get | jq -r '.url'
    fi
else
    echo "Service is DOWN (Status: $STATUS)"
fi


echo -e "\n========================================"
echo "4. DATA INTERSECTION (Python vs comm)"
echo "========================================"
# 'comm' compares two SORTED files.
# -12: Suppress unique to file 1 and unique to file 2 (Show only common)
# <(...): Process Substitution (feeds command output as a file)
echo "Common servers:"
comm -12 <(echo -e "server-alpha\nserver-beta" | sort) <(echo -e "server-beta\nserver-gamma" | sort)


echo -e "\n========================================"
echo "5. ALGORITHMS (Python vs awk/seq)"
echo "========================================"
echo "DevOps FizzBuzz (One-liner):"
# awk can do standard C-style logic
seq 15 | awk '{
    str=""
    if($1%3==0) str=str"Dev"
    if($1%5==0) str=str"Ops"
    print (str?str:$1)
}'
