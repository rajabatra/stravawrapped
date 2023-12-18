from flask import Flask, render_template, redirect, url_for, session
#from flask_oauthlib.client import OAuth
import requests
from urllib.parse import urlencode

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production

# Strava OAuth settings
STRAVA_CLIENT_ID = 'your_strava_client_id'
STRAVA_CLIENT_SECRET = 'your_strava_client_secret'
STRAVA_REDIRECT_URI = 'http://localhost:5000/login/authorized'  # Update with your redirect URI

STRAVA_API_URL = 'https://www.strava.com/api/v3/'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login')
def login():
    params = {
        'client_id': STRAVA_CLIENT_ID,
        'redirect_uri': STRAVA_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'read_all',  # Adjust the scope based on your needs
    }
    strava_authorize_url = 'https://www.strava.com/oauth/authorize?' + urlencode(params)
    return redirect(strava_authorize_url)

@app.route('/login/authorized')
def authorized():
    code = request.args.get('code')

    if not code:
        return 'Access denied: No authorization code provided.'

    # Exchange authorization code for access token
    token_url = 'https://www.strava.com/oauth/token'
    data = {
        'client_id': STRAVA_CLIENT_ID,
        'client_secret': STRAVA_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
    }

    response = requests.post(token_url, data=data)
    token_data = response.json()

    if 'access_token' not in token_data:
        return 'Failed to obtain access token.'

    session['strava_token'] = token_data['access_token']
    session['strava_user_id'] = get_strava_user_id(token_data['access_token'])

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('strava_token', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'strava_token' not in session:
        return redirect(url_for('index'))

    # Fetch user-specific data from Strava using the access token
    strava_token = session['strava_token']
    # Use the 'strava_token' to make API requests to Strava

    return render_template('dashboard.html', username=strava_token)

def get_strava_user_id(access_token):
    # Helper function to fetch user ID from Strava using the access token
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{STRAVA_API_URL}athlete', headers=headers)
    user_data = response.json()
    return user_data.get('id')

if __name__ == '__main__':
    app.run(debug=True)