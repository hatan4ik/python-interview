#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import time
from http import HTTPStatus
from typing import Any, Dict

# ==========================================
# SCENARIO:
# API Health Check with Type Hints and HTTPStatus Enum.
# ==========================================

TARGET_URL = "https://httpbin.org/get"

def check_service_health(url: str) -> bool:
    print(f"--- Checking Health of {url} ---")
    
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            
            # MODERN: Use HTTPStatus enum instead of magic number 200
            status_code = response.getcode()
            if status_code != HTTPStatus.OK:
                print(f"ALERT: Service returned status code {status_code}")
                return False
            
            data = response.read()
            # Type Hinting the parsed JSON for clarity
            json_data: Dict[str, Any] = json.loads(data)
            
            print("Response received successfully.")
            print(f"Server is reachable via: {json_data.get('url')}")
            return True

    except urllib.error.URLError as e:
        print(f"ALERT: Network error: {e}")
        return False
    except json.JSONDecodeError:
        print("ALERT: Invalid JSON.")
        return False
    except Exception as e:
        print(f"ALERT: Unexpected error: {e}")
        return False

def robust_health_check(url: str, retries: int = 3, delay: int = 2) -> bool:
    print(f"\n--- Robust Check with Retries ---")
    
    for attempt in range(1, retries + 1):
        print(f"Attempt {attempt}/{retries}...")
        if check_service_health(url):
            print("Service is Healthy!")
            return True
        
        if attempt < retries:
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
            
    print("CRITICAL: Service is DOWN after max retries.")
    return False

if __name__ == "__main__":
    robust_health_check(TARGET_URL)