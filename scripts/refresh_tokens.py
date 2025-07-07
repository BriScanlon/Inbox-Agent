import os
import json
import requests
from dotenv import load_dotenv

# Load secrets
load_dotenv()
CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")

# Load existing tokens
with open("tokens.json", "r") as token_file:
    tokens = json.load(token_file)

refresh_token = tokens.get("refresh_token")

if not refresh_token:
    print("No refresh_token found in tokens.json. You must re-authenticate.")
    exit(1)

# Request new access token
token_url = "https://oauth2.googleapis.com/token"
data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "refresh_token": refresh_token,
    "grant_type": "refresh_token",
}

response = requests.post(token_url, data=data)

if response.status_code == 200:
    new_tokens = response.json()
    tokens.update({
        "access_token": new_tokens["access_token"],
        "expires_in": new_tokens.get("expires_in", 3600),
        "scope": new_tokens.get("scope", tokens.get("scope")),
        "token_type": new_tokens.get("token_type", "Bearer"),
    })

    # Save updated tokens back to file
    with open("tokens.json", "w") as token_file:
        json.dump(tokens, token_file, indent=2)

    print("Access token refreshed successfully.")
    print("New Access Token:", tokens["access_token"])
else:
    print("Failed to refresh token.")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
