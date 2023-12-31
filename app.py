import requests
import pprint
from datetime import datetime, timedelta
import time
import os
import redis
from twilio.rest import Client
# calculate 10 seconds in the future
url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
# print(f"Fetching data from {url} for {now}.")
r = requests.get(url)
nfl_json = r.json()
# pprint.pprint(nfl_json["events"][0])
target_score = 38
target_score_minus_fg = target_score - 3
target_score_minus_td = target_score - 7

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

# data = 'i love dada:heart:'
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
value = 1

# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# #account_sid = 'MG07a5b06e7cd9a774b5e6bbfe6a2eaf6c'
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# messaging_service_sid='MG07a5b06e7cd9a774b5e6bbfe6a2eaf6c'
# client = Client(account_sid, auth_token)
# message = client.messages \
#     .create(
#         body="am i blocked",
#         messaging_service_sid=messaging_service_sid,
#         # from_='+18885221227',
#         to="+15712127641"
#                 )
sports_dict = {
    "New York Jets": 'Paul',
    "Buffalo Bills": 'Mason',
    "Kansas City Chiefs": 'Josh',
    "Atlanta Falcons": 'Ben',
    "Carolina Panthers": 'Greg',
    "Cleveland Browns": 'Ray',
    "Cincinnati Bengals": 'Jay',
    "Jacksonville Jaguars": 'Dave',
    "Minnesota Vikings": 'Frank',
    "Tampa Bay Buccaneers": 'Anthony',
    "New Orleans Saints": 'Brett',
    "Tennessee Titans": 'Brent',
    "Pittsburgh Steelers": 'Renzo',
    "San Francisco 49ers": 'Jason',
    "Washington Commanders": 'Beau',
    "Arizona Cardinals": 'Dave',
    "Baltimore Ravens": 'Greg',
    "Houston Texans": 'Tim',
    "Chicago Bears": 'Phil',
    "Green Bay Packers": 'Nick',
    "Denver Broncos": 'Ryan',
    "Las Vegas Raiders": 'Bobby',
    "New England Patriots": 'Jovany',
    "Philadelphia Eagles": 'Chris',
    "Los Angeles Chargers": 'Steve',
    "Miami Dolphins": 'Allen',
    "Seattle Seahawks": 'Armand',
    "Los Angeles Rams": 'Kevin',
    "New York Giants": 'Trevor',
    "Dallas Cowboys": 'Jamie',
    "Chicago Bears": 'Phil',
    "New England Patriots": 'Jovany',
    "Indianapolis Colts": 'Scott',
    "Detroit Lions": "Erik"
}

# response = requests.post('http://ntfy.sh/nfl38club', headers=headers, data=data)
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
                winning_message = f"The {team_display_name} finished the {matchup} game with {target_score} points, congrats to {sports_dict[team_display_name]}"
                # print(winning_key)
                print(winning_message)
                time.sleep(5)
                response = requests.post('http://ntfy.sh/nfl38club', headers=headers, data=winning_message)
        elif  timeleft != 'Final':
            # print(matchup)
            if r.exists(progress_key) == False and int(score) == int(target_score_minus_fg):
                message = f"The {team_display_name} are a field goal away from the magic {target_score} with a score of {score} in the matchup: {matchup} with the clock at {timeleft} "
                response = requests.post('http://ntfy.sh/nfl38club', headers=headers, data=message)
                # print("PROGRESSKEY: ",progress_key)
                r.set(progress_key,value)
                print(message)
            elif r.exists(progress_key) == False and int(score) == int(target_score_minus_td):
                message = f"The {team_display_name} are a touchdown away from the magic {target_score} with a score of {score} in the matchup: {matchup} with the clock at {timeleft} "
                response = requests.post('http://ntfy.sh/nfl38club', headers=headers, data=message)
                # print("PROGRESSKEY: ",progress_key)
                r.set(progress_key,value)
                print(message)


        # print(f"team {}")
        # pprint.pprint(competitors)
    