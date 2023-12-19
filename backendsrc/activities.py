import datetime
import requests
from flask import session
API_URL = 'https://www.strava.com/api/v3'
CLIENT_ID = '118376'
CLIENT_SECRET = 'b7e06ff027a718b797b30e40395d3ee8ba5ea314'
TOKEN_URL = 'https://www.strava.com/oauth/token'

def get_token(code):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(TOKEN_URL, data=data)
    return response.json()

def get_athlete_activities():
    headers = {'Authorization': f'Bearer {session["access_token"]}'}

    # Calculate the start date of the current year
    current_year_start = datetime.datetime(datetime.datetime.now().year, 1, 1)
    after_timestamp = int(current_year_start.timestamp())
    
    # Retrieve activities for the authenticated athlete starting from the current year
    response = requests.get(f'{API_URL}/athlete/activities', headers=headers, params={'after': after_timestamp})
    return response.json()