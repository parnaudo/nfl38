import requests
import pprint
from datetime import datetime, timedelta
import time
import os
import redis
from util import fetch_json_data, is_scorigami
# calculate 10 seconds in the future
url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
# print(f"Fetching data from {url} for {now}.")
r = requests.get(url)
nfl_json = fetch_json_data(url)
# nfl_json = r.json()
# pprint.pprint(nfl_json["events"][0])
target_score = 38
target_score_minus_fg = target_score - 3
target_score_minus_td = target_score - 7
whatsapp_service_api = ""
headers = {
    'token': '',
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

# data = 'i love dada:heart:'
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
value = 1

sports_dict = {
    "New England Patriots": 'Allen',
    "Buffalo Bills": 'Greg',
    "Miami Dolphins": 'Chris',
    "New York Jets": 'Paul',
    "Pittsburgh Steelers": 'Rene',
    "Baltimore Ravens": 'Matt',
    "Cincinnati Bengals": 'Ben',
    "Cleveland Browns": 'Josh',
    "Jacksonville Jaguars": 'Ryan',
    "Houston Texans": 'Phil',
    "Indianapolis Colts": 'Jay',
    "Tennessee Titans": 'Anthony',
    "Denver Broncos": 'Greg',
    "Los Angeles Chargers": 'Beau',
    "Kansas City Chiefs": 'Brent',
    "Las Vegas Raiders": 'Ryan',
    "Philadelphia Eagles": 'Jamie',
    "Dallas Cowboys": 'Steve',
    "Washington Commanders": 'Mason',
    "New York Giants": 'Mike',
    "Chicago Bears": 'Kevin',
    "Green Bay Packers": 'Steve',
    "Minnesota Vikings": 'Ray',
    "Detroit Lions": 'Erik',
    "Carolina Panthers": 'Jason',
    "Tampa Bay Buccaneers": 'Dave',
    "Atlanta Falcons": 'Nick',
    "New Orleans Saints": 'Brett',
    "Seattle Seahawks": 'Kyle',
    "Los Angeles Rams": 'Tim',
    "San Francisco 49ers": 'Bobby',
    "Arizona Cardinals": 'Scott',
}
# test_data = {
#     "Phone": "120363153309445450@g.us",
#     "Body": "🤖🤖🤖testing python implementation🤖🤖🤖"
# }
# response = requests.post(f'http://{whatsapp_service_api}:8080/chat/send/text', headers=headers, json=test_data)
production_phone = "120363170911301520@g.us"
staging_phone = "120363153309445450@g.us"
home_team_display_name = nfl_json["events"][0]['competitions'][0]['competitors'][0]['team']['displayName']
    # away_team_score = game['competitions'][0]['competitors'][1]['score']
away_team_display_name = nfl_json["events"][0]['competitions'][0]['competitors'][1]['team']['displayName']
for events in nfl_json["events"]:
    matchup = events['name']
    timeleft = events['status']['type']['detail']
    for competitors in events['competitions'][0]['competitors']:
        score = competitors['score']
        team_display_name = competitors['team']['displayName']
        # pprint.pprint(competitors)
        progress_key = f"{team_display_name}{events['shortName']}{nfl_json['season']['year']}".replace(" ","")
        winning_key = f"{events['status']['type']['detail']}{team_display_name}{events['shortName']}{nfl_json['season']['year']}".replace(" ","")
        # print("matchup: ",matchup)
        # print("SCORE: ",score)
        # print("TIMELEFT: ",timeleft)
        # print(team_display_name)
        if timeleft == 'Final':
            if r.exists(winning_key) == False and int(score) == target_score:
                r.set(winning_key,value)
                winning_message = f"🤖🚨The {team_display_name} finished the {matchup} game with {target_score} points, congrats to {sports_dict[team_display_name]}🤖🚨"
                # print(winning_key)
                print(winning_message)
                time.sleep(5)
                winning_json = {
                            "Phone": staging_phone,
                            "Body": winning_message
                            }
                response = requests.post(f'http://{whatsapp_service_api}:8080/chat/send/text', headers=headers, json=winning_json)
                is_scorigami(target_score, production_phone)
        elif  timeleft != 'Final':
            # print(matchup)
            if r.exists(progress_key) == False and int(score) == int(target_score_minus_fg):
                message = f"🤖🚨The {team_display_name} are a field goal away from the magic {target_score} with a score of {score} in the matchup: {matchup} with the clock at {timeleft}🤖🚨"
                status_json = {
                            "Phone": staging_phone,
                            "Body": message
                            }
                response = requests.post(f'http://{whatsapp_service_api}:8080/chat/send/text', headers=headers, json=status_json)
                # print("PROGRESSKEY: ",progress_key)
                r.set(progress_key,value)
                print(message)
                time.sleep(5)
            elif r.exists(progress_key) == False and int(score) == int(target_score_minus_td):
                message = f"🤖🚨The {team_display_name} are a touchdown away from the magic {target_score} with a score of {score} in the matchup: {matchup} with the clock at {timeleft}🤖🚨"
                status_json = {
                            "Phone": staging_phone,
                            "Body": message
                            }
                response = requests.post(f'http://{whatsapp_service_api}:8080/chat/send/text', headers=headers, json=status_json)
                r.set(progress_key,value)
                print(message)
                time.sleep(5)
            elif r.exists(progress_key) == False and int(score) == int(target_score):
                message = f"🤖🚨The {team_display_name} are at the magic score of {target_score} in the matchup: {matchup} with the clock at {timeleft} STOP THE COUNT!!!!🤖🚨"
                status_json = {
                            "Phone": staging_phone,
                            "Body": message
                            }
                response = requests.post(f'http://{whatsapp_service_api}:8080/chat/send/text', headers=headers, json=status_json)
                r.set(progress_key,value)
                print(message)
                time.sleep(5)
        # print(f"team {}")
        # pprint.pprint(competitors)
    # curl -d "Backup successful 😀" ntfy.sh/nfl38
