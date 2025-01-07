import requests
from bs4 import BeautifulSoup
import pandas as pd
from util import fetch_nfl_scores,calculate_distance_to_38

# Example usage:
if __name__ == "__main__":
    scores = fetch_nfl_scores()
    if scores:
        print("\nTeams sorted by average distance to 38 points (excluding teams that scored exactly 38):")
        sorted_teams = calculate_distance_to_38(scores)
        for team, avg_distance in sorted_teams:
            print(f"{team}: {avg_distance:.2f}")