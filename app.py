import requests
import pprint
from datetime import datetime, timedelta
import os
import redis
# calculate 10 seconds in the future
url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
# print(f"Fetching data from {url} for {now}.")
r = requests.get(url)
nfl_json = r.json()
# pprint.pprint(nfl_json["events"][0])
target_score = 21
target_score_minus_fg = target_score - 3
target_score_minus_td = target_score - 7

phone_numbers = ["+15712127641"]

        # if message.error_code is not None:
        # print(message.error_code)
        # print(message.error_message)

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

# data = 'i love dada:heart:'
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
value = 1

sports_dict = {
    "New York Jets": 'Paul',
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
        print("WINNINGKEY: ",winning_key)

        if timeleft == 'Final' and int(score) == target_score:
            if r.exists(winning_key) == False:
                r.set(winning_key,value)
                winning_message = f"The {team_display_name} finished the {matchup} game with {target_score} points, congrats to {sports_dict[team_display_name]}"
                print(winning_message)
                response = requests.post('http://ntfy.sh/nfl38club', headers=headers, data=winning_message)
        elif r.exists(progress_key) == False:
            if int(score) == int(target_score_minus_fg):
                message = f"The {team_display_name} are a field goal away from the magic {target_score} with a score of {score} in the matchup: {matchup} with the clock at {timeleft} "
                response = requests.post('http://ntfy.sh/nfl38club', headers=headers, data=message)
                print("PROGRESSKEY: ",progress_key)
                r.set(progress_key,value)
                print(message)
            elif int(score) == int(target_score_minus_td):
                message = f"The {team_display_name} are a touchdown away from the magic {target_score} with a score of {score} in the matchup: {matchup} with the clock at {timeleft} "
                response = requests.post('http://ntfy.sh/nfl38club', headers=headers, data=message)
                print(progress_key)
                r.set(progress_key,value)
                print(message)
            # send_twilio_sms(phone_numbers,home_team_display_name,home_team_score,messaging_service_sid)
        # if away_team_score == target_score_minus_fg or away_team_score == target_score_minus_td:
        #     away_message = f"{away_team_display_name} might hit it with a score of {away_team_score} "
        #     response = requests.post('http://ntfy.sh/nfl38club', headers=headers, data=away_message)
        #     print(away_message)
            # send_twilio_sms(phone_numbers,away_team_display_name,away_team_score,messaging_service_sid)
        else:
            print("We already alerted")

        # print(f"team {}")
        # pprint.pprint(competitors)
    