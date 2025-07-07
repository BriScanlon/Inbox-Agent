"""
Gmail Service Handler - Handles Gmail OAuth2 authentication and Gmail API interactions.
"""

import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def load_gmail_service():
    """Loads Gmail API service using saved tokens."""
    with open("tokens.json", "r") as token_file:
        tokens = json.load(token_file)

    creds = Credentials(
        tokens["access_token"],
        refresh_token=tokens.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GMAIL_CLIENT_ID"),
        client_secret=os.getenv("GMAIL_CLIENT_SECRET"),
        scopes=[
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/gmail.modify",
            "https://www.googleapis.com/auth/userinfo.email",
        ],
    )

    # Build Gmail API client
    service = build("gmail", "v1", credentials=creds)
    return service


def authenticate_gmail():
    # Placeholder for Gmail OAuth2 authentication logic
    pass


def fetch_emails(max_results=5):
    """Fetches recent emails and prints basic info (From, Subject)."""
    service = load_gmail_service()

    # Fetch latest emails (list message IDs)
    results = (
        service.users().messages().list(userId="me", maxResults=max_results).execute()
    )
    messages = results.get("messages", [])

    if not messages:
        print("No emails found.")
        return

    print(f"Found {len(messages)} email(s):\n")

    for msg in messages:
        msg_id = msg["id"]
        msg_detail = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=msg_id,
                format="metadata",
                metadataHeaders=["Subject", "From"],
            )
            .execute()
        )

        headers = msg_detail.get("payload", {}).get("headers", [])
        subject = next(
            (h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)"
        )
        sender = next(
            (h["value"] for h in headers if h["name"] == "From"), "(Unknown Sender)"
        )

        print(f"📧 From: {sender}")
        print(f"   Subject: {subject}\n")


def move_to_marketing_folder(email_id):
    # Placeholder to move emails to marketing folder
    pass


def send_summary_email(summary):
    # Placeholder to send summary email via Gmail API
    pass
