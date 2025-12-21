import urllib.request
import urllib.error
import json
import time

# ==========================================
# SCENARIO:
# Write a script to monitor the health of a microservice.
# The service returns JSON: {"status": "ok", "uptime": 1234}
# If status is not "ok" or if the request fails, alert the user.
# ==========================================

# NOTE: In a real job, use the 'requests' library (pip install requests).
# It is much more human-friendly. e.g., requests.get(url).json()
# However, knowing urllib (standard lib) is a great "flex" in interviews
# if you are in a restricted environment.

TARGET_URL = "https://httpbin.org/get" # Public echo service for testing

def check_service_health(url):
    print(f"--- Checking Health of {url} ---")
    
    try:
        # 1. MAKE THE REQUEST
        # timeout is crucial for production scripts!
        with urllib.request.urlopen(url, timeout=5) as response:
            
            # 2. CHECK HTTP STATUS
            status_code = response.getcode()
            if status_code != 200:
                print(f"ALERT: Service returned status code {status_code}")
                return False
            
            # 3. PARSE JSON
            data = response.read()
            json_data = json.loads(data)
            
            # Simulate checking a specific field (httpbin returns 'url', not 'status', adapting logic)
            # In a real interview question: if json_data.get("status") == "ok": ...
            print("Response received successfully.")
            print(f"Server is reachable via: {json_data.get('url')}")
            return True

    except urllib.error.URLError as e:
        # Handles DNS errors, connection refused, etc.
        print(f"ALERT: Network error contacting service: {e}")
        return False
    except json.JSONDecodeError:
        print("ALERT: Service returned invalid JSON.")
        return False
    except Exception as e:
        print(f"ALERT: Unexpected error: {e}")
        return False

# ==========================================
# RETRY LOGIC (Very common interview follow-up)
# "How would you handle transient failures?"
# ==========================================
def robust_health_check(url, retries=3, delay=2):
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
