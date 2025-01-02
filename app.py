from flask import Flask, request, redirect, session, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed to encrypt session cookies securely

# Spotify API credentials (replace with your values)
SPOTIFY_CLIENT_ID = "3c42b89ffcc246b7a209eb26d2adb982"
SPOTIFY_CLIENT_SECRET = "3b49f7a5eea1418da14c043defa19c7e"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:5000/callback"

# Set up Spotipy's SpotifyOAuth
scope = "user-library-read playlist-read-private"  # Add other scopes as needed
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope,
)

# Flask Routes
@app.route('/')
def home():
    """Home page with a login link."""
    return '''
        <h1>Welcome to ImageToMusic</h1>
        <a href="/login">Login with Spotify</a>
    '''

@app.route('/login')
def login():
    """Redirect user to Spotify's authorization page."""
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def spotify_callback():
    """Handle Spotify's redirect after authorization."""
    code = request.args.get('code')
    if code:
        # Exchange the authorization code for an access token
        token_info = sp_oauth.get_access_token(code)
        session['token_info'] = token_info  # Save token i
