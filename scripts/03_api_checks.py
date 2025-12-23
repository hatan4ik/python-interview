#!/usr/bin/env python3
"""
API Health Monitoring Module.

Demonstrates how to interact with REST APIs using the standard library.
Focuses on resilience (retries), status code validation, and JSON parsing.
"""

import urllib.request
import urllib.error
import json
import time
from http import HTTPStatus
from typing import Any, Dict

TARGET_URL = "https://httpbin.org/get"

def check_service_health(url: str) -> bool:
    """
    Performs a single HTTP GET request to check service health.

    Args:
        url (str): The endpoint to check.

    Returns:
        bool: True if the service returns 200 OK and valid JSON, False otherwise.
    """
    print(f"--- Checking Health of {url} ---")
    
    try:
        # Timeout is mandatory in production code to prevent hanging processes.
        with urllib.request.urlopen(url, timeout=5) as response:
            
            status_code = response.getcode()
            if status_code != HTTPStatus.OK:
                print(f"ALERT: Service returned status code {status_code}")
                return False
            
            data = response.read()
            json_data: Dict[str, Any] = json.loads(data)
            
            print("Response received successfully.")
            print(f"Server is reachable via: {json_data.get('url')}")
            return True

    except urllib.error.URLError as e:
        print(f"ALERT: Network error: {e}")
        return False
    except json.JSONDecodeError:
        print("ALERT: Invalid JSON received.")
        return False
    except Exception as e:
        print(f"ALERT: Unexpected error: {e}")
        return False

def robust_health_check(url: str, retries: int = 3, delay: int = 2) -> bool:
    """
    Checks service health with exponential-like backoff (fixed delay).

    Args:
        url (str): The endpoint to check.
        retries (int): Maximum number of attempts.
        delay (int): Seconds to wait between attempts.

    Returns:
        bool: True if service eventually passes, False if all retries fail.
    """
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
