#!/usr/bin/env python3
"""
Concurrency & Parallelism.

Demonstrates using `ThreadPoolExecutor` to perform I/O bound tasks (network requests)
in parallel. This is significantly faster than sequential execution for API checks.
"""

import concurrent.futures
import urllib.request
import time
from http import HTTPStatus
from typing import List, Tuple

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
    Checks a single URL and returns metrics.
    
    Args:
        url (str): The URL to check.
        
    Returns:
        Tuple[str, str, float]: (URL, Status String, Duration in seconds)
    """
    start_time = time.time()
    try:
        # timeout=5 ensures that one slow server doesn't block the thread indefinitely
        with urllib.request.urlopen(url, timeout=5) as response:
            return (url, f"UP ({response.getcode()})", time.time() - start_time)
            
    except urllib.error.HTTPError as e:
        # HTTPError captures 4xx/5xx responses (which are still valid server responses)
        return (url, f"ERR ({e.code})", time.time() - start_time)
        
    except Exception as e:
        # Catches DNS errors, ConnectionRefused, etc.
        return (url, f"FAIL ({str(e)})", time.time() - start_time)

def main() -> None:
    """
    Orchestrates the parallel execution of health checks.
    """
    print(f"--- Starting Concurrent Checks for {len(URLS)} URLs ---")
    start_total = time.time()
    
    # Context Manager for the ThreadPool handles setup/teardown automatically.
    # max_workers=5 allows 5 checks to run simultaneously.
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        
        # Dictionary Comprehension mapping Future objects to their source URLs
        future_to_url = {executor.submit(check_status, url): url for url in URLS}
        
        # as_completed() yields futures as they finish, not in submission order.
        # This allows us to process results immediately (reactive).
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                url_res, status, duration = future.result()
                print(f"[{duration:.2f}s] {url_res} -> {status}")
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
                
    print(f"--- All checks finished in {time.time() - start_total:.2f} seconds ---")

if __name__ == "__main__":
    main()