import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
import redis
whatsapp_service_api = "54.237.21.143"
headers = {
    'token': 'someverydifficulttokentoremember',
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
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

def send_whatsapp_message(phone_number: str, message: str):
    url = f'http://{whatsapp_service_api}:8080/chat/send/text'
    data = {
        "Phone": phone_number,
        "Body": message
    }
    response = requests.post(url, headers=headers, json=data)
    return response

def is_scorigami(score_total: int, phone_number: str):

    current_scores = fetch_missing_scores()

    if score_total in current_scores and r.get(f"scorigami_{score_total}") is None:
        print("yup")
        r.set(f"scorigami_{score_total}", 1)
        send_whatsapp_message(phone_number, "🤖🚨Thats a Scorigami yo🤖🚨")
        return True
    else:
        return False
def fetch_missing_scores():
    url = "https://www.pro-football-reference.com/boxscores/missing-scores.htm"
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table in the HTML (tables usually have the tag <table>)
    table = soup.find('table', {'id': 'games'})  # Replace 'games' if necessary
    
    # Initialize a list to store the total scores
    score_totals = []

    if table:
        # Find all rows in the table (excluding the header row)
        rows = table.find_all('tr')[1:]  # Skipping the header row
        
        for row in rows:
            # Extract individual cells
            cells = row.find_all('td')
            # print(cells[0].text.strip())
            if len(cells) > 0:
                # Extract the score from cells[1], split it, and calculate the total
                try:
                    score_text = cells[0].text.strip()
                    # print("score_text: ",score_text)
                    visitor_score, home_score = map(int, score_text.split('-'))
                    total_score = visitor_score + home_score
                    print(total_score)
                    score_totals.append(total_score)
                except (ValueError, IndexError):
                    # Handle the case where the score is missing, not in the expected format, or cells[1] doesn't exist
                    score_totals.append(None)
    
    return score_totals
def fetch_nfl_scores():
    # URL of the NFL games
    url = "https://www.pro-football-reference.com/years/2024/games.htm"
    
    # Add headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Initialize dictionary for team scores
    team_scores = {}
    
    try:
        # Fetch the webpage
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the games table
        table = soup.find('table', {'id': 'games'})
        
        # Convert table to pandas DataFrame
        df = pd.read_html(str(table))[0]
        # Process each row in the DataFrame
        for _, row in df.iterrows():
            try:
                # Try to convert scores to integers first
                winner_score = int(row['PtsW'])
                loser_score = int(row['PtsL'])
                
                winner = row['Winner/tie']
                loser = row['Loser/tie']
                # print(winner, winner_score, loser, loser_score)
                
                # Only proceed if integer conversion was successful
                if winner not in team_scores:
                    team_scores[winner] = []
                if loser not in team_scores:
                    team_scores[loser] = []
                
                # Append scores to respective teams
                team_scores[winner].append(winner_score)
                team_scores[loser].append(loser_score)
                
            except (ValueError, TypeError):
                # Skip this row if scores can't be converted to integers
                continue
        
        return team_scores
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None
def calculate_distance_to_38(scores_dict):
    # Calculate average distance to 38 for each team
    team_distances = {}
    
    for team, scores in scores_dict.items():
        if scores:  # Check if the team has any scores
            # Skip teams that have scored exactly 38
            if 38 not in scores:
                continue
                
            # Calculate absolute distance to 38 for each score
            distances = [abs(38 - score) for score in scores]
            # Calculate average distance
            avg_distance = sum(distances) / len(distances)
            team_distances[team] = avg_distance
    
    # Sort teams by average distance (ascending)
    sorted_teams = sorted(team_distances.items(), key=lambda x: x[1])
    
    return sorted_teams
# Example usage

