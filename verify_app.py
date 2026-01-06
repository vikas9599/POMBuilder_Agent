import requests
import time
import sys

def verify_app():
    url = 'http://127.0.0.1:5000/refactor'
    file_path = 'testing_script.js'
    
    print(f"Attempting to connect to {url}...")
    
    # Wait for server to start
    for i in range(10):
        try:
            requests.get('http://127.0.0.1:5000/')
            print("Server is up!")
            break
        except requests.exceptions.ConnectionError:
            print("Waiting for server...")
            time.sleep(1)
    else:
        print("Server failed to start.")
        sys.exit(1)

    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'model': 'mock'}
            print(f"Uploading {file_path}...")
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                print("Success! Response received.")
                json_response = response.json()
                
                print("\n--- Test Data Preview ---")
                print(json_response.get('test_data')[:200] + "...")
                
                print("\n--- Test Page Preview ---")
                print(json_response.get('test_page')[:200] + "...")
                
                print("\n--- Test Script Preview ---")
                print(json_response.get('test_script')[:200] + "...")
                
                if json_response.get('test_data') and json_response.get('test_page') and json_response.get('test_script'):
                    print("\nVerification PASSED: All 3 files generated.")
                else:
                    print("\nVerification FAILED: Missing generated content.")
            else:
                print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    verify_app()
