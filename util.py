import requests
import time
def fetch_json_data(url, max_retries=3, timeout=10):
    """
    Fetch JSON data from a given URL with error handling and retry logic.
    
    Args:
        url (str): The URL to fetch data from.
        max_retries (int): Number of retries in case of connection issues (default is 3).
        timeout (int): Timeout for each request in seconds (default is 10 seconds).
    
    Returns:
        dict or None: The JSON response as a dictionary, or None if the request fails.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()  # Return the JSON response

        except requests.exceptions.Timeout:
            print(f"Timeout error on attempt {attempt + 1}/{max_retries}. Retrying...")
        
        except requests.exceptions.ConnectionError:
            print(f"Connection error on attempt {attempt + 1}/{max_retries}. Retrying...")
        
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP error: {errh}")
            break  # Stop retrying on HTTP error
        
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")
            break  # Stop retrying on other request exceptions
        
        # Wait before retrying
        time.sleep(2)
    
    # If all attempts fail, return None
    print("Failed to fetch data after multiple attempts.")
    return None