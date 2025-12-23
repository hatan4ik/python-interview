#!/usr/bin/env python3
"""
Framework Showcase: Requests, Boto3, and FastAPI.

This script demonstrates the SYNTAX of the "Big Three" DevOps libraries.

NOTE:
These are external libraries. In a real project, you must:
> pip install requests boto3 fastapi uvicorn

To make this script runnable immediately without installation,
we use 'unittest.mock' to SIMULATE their behavior.
"""

from unittest.mock import MagicMock
import json

# ==========================================
# 1. REQUESTS (The HTTP Client)
# ==========================================
def demo_requests():
    print("\n--- 1. Requests (HTTP Client) ---")
    print("Scenario: Calling a 3rd party API to get data.")
    
    # MOCK SETUP (Ignore this in interview, it's just to make script run)
    requests = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"id": 101, "name": "DevOps Hero"}
    requests.get.return_value = mock_resp

    # --- REAL INTERVIEW CODE STARTS HERE ---
    
    # 1. Make the GET request
    print(">> request = requests.get('https://api.example.com/users/1')")
    response = requests.get('https://api.example.com/users/1')
    
    # 2. Check status and parse
    if response.status_code == 200:
        data = response.json()
        print(f"Success! User Name: {data['name']}")
    else:
        print("Failed to fetch user.")


# ==========================================
# 2. BOTO3 (AWS SDK)
# ==========================================
def demo_boto3():
    print("\n--- 2. Boto3 (AWS Interaction) ---")
    print("Scenario: Listing S3 Buckets.")

    # MOCK SETUP
    boto3 = MagicMock()
    mock_s3 = MagicMock()
    # Simulate AWS response structure (Dict with 'Buckets' list)
    mock_s3.list_buckets.return_value = {
        'Buckets': [
            {'Name': 'prod-logs-archive', 'CreationDate': '2024-01-01'},
            {'Name': 'dev-testing-bucket', 'CreationDate': '2024-02-15'}
        ]
    }
    boto3.client.return_value = mock_s3

    # --- REAL INTERVIEW CODE STARTS HERE ---
    
    # 1. Create the client (Connect to AWS)
    print(">> s3 = boto3.client('s3')")
    s3 = boto3.client('s3')
    
    # 2. Call the API
    print(">> response = s3.list_buckets()")
    response = s3.list_buckets()
    
    # 3. Process results
    print("Found Buckets:")
    for bucket in response['Buckets']:
        print(f"  - {bucket['Name']}")


# ==========================================
# 3. FASTAPI (Microservices)
# ==========================================
def demo_fastapi():
    print("\n--- 3. FastAPI (Web Server) ---")
    print("Scenario: A simple Health Check endpoint.")
    print("(This is code structure only - requires 'uvicorn' to run)")
    
    code_example = """
from fastapi import FastAPI

# 1. Initialize App
app = FastAPI()

# 2. Define Route (Decorator)
@app.get("/health")
def health_check():
    # Returns JSON automatically
    return {"status": "ok", "service": "payment-gateway"}

# 3. Run (Shell command):
# uvicorn main:app --reload
"""
    print(code_example)

if __name__ == "__main__":
    demo_requests()
    demo_boto3()
    demo_fastapi()
