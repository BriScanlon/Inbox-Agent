import os
import json
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load secrets
load_dotenv()
CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/userinfo.email",
]

# Step 1: Generate Authorization URL
params = {
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "scope": " ".join(SCOPES),
    "access_type": "offline",
    "prompt": "consent",
}

auth_url = "https://accounts.google.com/o/oauth2/auth?" + urlencode(params)
print("Please visit this URL to authorize this application:")
print(auth_url)

# Step 2: Manually extract authorization code from URL
print("\nAfter authorizing, you'll get redirected to localhost (which will fail to load).")
print("Copy the 'code' parameter from the URL bar and paste it here.")
auth_code = input("\nPaste authorization code here: ").strip()

# Step 3: Exchange Authorization Code for Tokens
token_url = "https://oauth2.googleapis.com/token"
data = {
    "code": auth_code,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
}

response = requests.post(token_url, data=data)
if response.status_code == 200:
    tokens = response.json()
    print("Token obtained successfully.")
    print("Access Token:", tokens["access_token"])

    # Save tokens securely
    with open("tokens.json", "w") as f:
        json.dump(tokens, f, indent=2)
    print("Tokens saved to tokens.json")
else:
    print("Failed to obtain tokens.")
    print("Status:", response.status_code)
    print("Response:", response.text)
