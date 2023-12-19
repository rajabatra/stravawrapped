from flask import Flask, redirect, url_for, session, request, jsonify, render_template
import requests
import os

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
        athlete_info = get_athlete_info()
        return render_template('home.html', athlete_info=athlete_info)
    else:
        return render_template('home.html', login_url=url_for('login'))

@app.route('/login')
def login():
    return redirect(f'{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=read')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        token_response = get_token(code)
        if 'access_token' in token_response:
            session['access_token'] = token_response['access_token']
    return redirect(url_for('home'))

def get_token(code):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(TOKEN_URL, data=data)
    return response.json()

def get_athlete_info():
    headers = {'Authorization': f'Bearer {session["access_token"]}'}
    response = requests.get(f'{API_URL}/athlete', headers=headers)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)