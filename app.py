import datetime
from flask import Flask, redirect, url_for, session, request, jsonify, render_template
import requests
import os
import pandas as pd

from backendsrc import activities

app = Flask(__name__)

# Replace these values with your Strava API credentials
CLIENT_ID = '118376'
CLIENT_SECRET = 'b7e06ff027a718b797b30e40395d3ee8ba5ea314'
REDIRECT_URI = 'http://localhost:8000/callback'  # Update with your actual callback URI
AUTH_URL = 'https://www.strava.com/oauth/authorize'
TOKEN_URL = 'https://www.strava.com/oauth/token'
API_URL = 'https://www.strava.com/api/v3'

app.secret_key = os.urandom(24)

# @app.route('/')
# def home():
#     if 'access_token' in session:
#         athlete_info = get_athlete_info()
#         return f'Logged in as {athlete_info["firstname"]} {athlete_info["lastname"]}. {athlete_info}'
#     else:
#         return '<a href="/login">Login with Strava</a>'
@app.route('/')
def home():
    if 'access_token' in session:
        # Render the loading page while home page is being built
        return render_template('loading.html', next_url=url_for('home_async'))
    else:
        return render_template('home.html', login_url=url_for('login'))

@app.route('/home-async', methods=['GET', 'POST'])
def home_async():
    if 'access_token' in session:
        # Perform time-consuming operations (e.g., get athlete activities)
        athlete_info = get_athlete_activities()
        totaldistance = activities.create_tables(athlete_info)
        plotdata = activities.create_plot(totaldistance['latlng'])
        return render_template('home.html', athlete_info=totaldistance, plotdata=plotdata)
    else:
        return render_template('home.html', login_url=url_for('login'))

@app.route('/login')
def login():
    return redirect(f'{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=read,activity:read&approval_prompt=auto')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        token_response = get_token(code)
        if 'access_token' in token_response:
            session['access_token'] = token_response['access_token']
    return redirect(url_for('home_async'))

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
    # response = requests.get(f'{API_URL}/athlete/activities', headers=headers, params={'after': after_timestamp, 'per_page': 400}, )
    # return response.json()
    activities = []
    page = 1

    while True:
        # Retrieve activities for the authenticated athlete starting from the current year and paginating through results
        response = requests.get(f'{API_URL}/athlete/activities', headers=headers, params={'after': after_timestamp, 'page': page, 'per_page': 200})
        activities_page = response.json()

        if not activities_page:
            # No more activities to fetch
            break

        activities.extend(activities_page)
        page += 1
    
    combined_json = {"activities": activities}


    # Convert the list of activities to a DataFrame
    
    runs_data = []
    for activity in combined_json['activities']:
        run_info = {
            'name': activity['name'],
            'distance': activity['distance'],
            'moving_time': activity['moving_time'],
            'total_elevation_gain': activity['total_elevation_gain'],
            'start_date': activity['start_date'],
            'summary_polyline': activity['map']['summary_polyline']
        }
        runs_data.append(run_info)

    # Create a DataFrame
    df = pd.DataFrame(runs_data)
    return df
    #return activities






if __name__ == '__main__':
    app.run(debug=True)