#!/usr/bin/env python3
import concurrent.futures
import urllib.request
import time
from http import HTTPStatus
from typing import List, Dict, Tuple

# ==========================================
# SCENARIO: Scaling Up
# FAANG Question: "Your script checks one server fine. 
# How do you check 1,000 servers without taking 1,000 seconds?"
#
# ANSWER: Concurrency (Threading for I/O bound tasks).
# We use 'concurrent.futures.ThreadPoolExecutor' which is the modern standard.
# ==========================================

# List of targets (Public APIs for testing)
URLS: List[str] = [
    "https://httpbin.org/get",
    "https://httpbin.org/delay/1",  # Simulates a slow server
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404", # Simulates a missing service
    "https://httpbin.org/status/500", # Simulates a crashing service
]

def check_status(url: str) -> Tuple[str, str, float]:
    """
    Checks a single URL. Returns (url, status, time_taken).
    """
    start_time = time.time()
    try:
        # timeout is critical to prevent one bad server blocking a thread forever
        with urllib.request.urlopen(url, timeout=5) as response:
            return (url, f"UP ({response.getcode()})", time.time() - start_time)
            
    except urllib.error.HTTPError as e:
        # HTTPError is raised for non-200 codes but we still got a response
        return (url, f"ERR ({e.code})", time.time() - start_time)
        
    except Exception as e:
        return (url, f"FAIL ({str(e)})", time.time() - start_time)

def main():
    print(f"--- Starting Concurrent Checks for {len(URLS)} URLs ---")
    start_total = time.time()
    
    # max_workers=5 means we check 5 URLs at the exact same time.
    # If we had 100 URLs, this would be significantly faster than a loop.
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        
        # Submit all tasks to the pool
        # future_to_url is a dictionary mapping the 'Future' object to the URL
        future_to_url = {executor.submit(check_status, url): url for url in URLS}
        
        # as_completed yields futures as they finish (in any order)
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                # Get the result from the function
                url_res, status, duration = future.result()
                print(f"[{duration:.2f}s] {url_res} -> {status}")
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
                
    print(f"--- All checks finished in {time.time() - start_total:.2f} seconds ---")

if __name__ == "__main__":
    main()
