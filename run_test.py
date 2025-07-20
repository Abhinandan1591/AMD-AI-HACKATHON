import requests
import json
import time

# --- CONFIGURATION ---
# IMPORTANT: Replace this with the actual IP address of your MI300 instance
SERVER_IP = "129.212.189.236" 

# The rest should be correct
SERVER_PORT = 5000
ENDPOINT = "/receive"
INPUT_JSON_FILE = "input_request.json"

# Construct the full URL
SERVER_URL = f"http://{SERVER_IP}:{SERVER_PORT}{ENDPOINT}"

print(f"Targeting server at: {SERVER_URL}")

# --- SCRIPT ---
try:
    # Load the input JSON from the file
    with open(INPUT_JSON_FILE) as f:
        input_json = json.load(f)
    
    print("\n--- Sending Request ---")
    print(json.dumps(input_json, indent=2))
    
    # Measure the latency
    start_time = time.time()
    
    # Send the POST request to the server
    # The timeout is set to 12 seconds to be safe, but the goal is < 10s
    response = requests.post(SERVER_URL, json=input_json, timeout=12)
    
    end_time = time.time()
    latency = end_time - start_time
    
    print(f"\n--- Response Received (Latency: {latency:.2f} seconds) ---")

    # Check if the request was successful
    if response.status_code == 200:
        print("Status: 200 OK")
        # Print the JSON response from your AI assistant
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Status: {response.status_code} - Error")
        print("Response Body:", response.text)

except requests.exceptions.Timeout:
    print("\n--- ERROR: Request Timed Out ---")
    print(f"The server did not respond within the timeout period.")
except requests.exceptions.ConnectionError as e:
    print("\n--- ERROR: Connection Failed ---")
    print(f"Could not connect to the server at {SERVER_URL}.")
    print("Please check:")
    print("1. Is the IP address correct?")
    print("2. Is the Flask server running in your Jupyter notebook?")
    print("3. Is there a firewall blocking the connection?")
except FileNotFoundError:
    print(f"\n--- ERROR: Input file not found ---")
    print(f"Make sure '{INPUT_JSON_FILE}' is in the same directory as this script.")
except Exception as e:
    print(f"\n--- An unexpected error occurred ---")
    print(e)