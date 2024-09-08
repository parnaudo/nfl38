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
    'token': 'someverydifficulttokentoremember',
    'accept': 'application/json',
    'Content-Type': 'application/json'
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
#   
#              )
whatsapp_service_api = "54.237.21.143"
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
#production phone number: 120363170911301520@g.us
test_data = {
    "Phone": "120363153309445450@g.us",
    "Body": "😘😽😉"
}
response = requests.post(f'http://{whatsapp_service_api}:8080/chat/send/text', headers=headers, json=test_data)

# curl -X GET "http://whatsapi-lb-1750989665.us-east-1.elb.amazonaws.com:8080/group/list?token=someverydifficulttokentoremember" -H  "accept: application/json" |