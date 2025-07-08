"""
Gmail Service Handler - Handles Gmail OAuth2 authentication and Gmail API interactions.
"""

import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from ollama_client import classify_email_with_llm


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


def get_or_create_label(label_name="AI Processed"):
    """Gets the Gmail label ID for the given name, creating it if it doesn't exist."""
    service = load_gmail_service()
    labels = service.users().labels().list(userId="me").execute().get("labels", [])

    # Check if label exists
    for label in labels:
        if label["name"].lower() == label_name.lower():
            print(f"Found existing label: {label_name}")
            return label["id"]

    # If not found, create it
    label_body = {
        "name": label_name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show",
    }

    new_label = service.users().labels().create(userId="me", body=label_body).execute()
    print(f"Created new label: {label_name}")
    return new_label["id"]


def apply_label_to_email(message_id, label_id):
    """Applies the specified label to the given email."""
    service = load_gmail_service()
    body = {
        "addLabelIds": [label_id],
        "removeLabelIds": [],
    }

    service.users().messages().modify(userId="me", id=message_id, body=body).execute()

    print(f"✅ Applied label to email ID: {message_id}")


from ollama_client import classify_email_with_llm  # Make sure you have this import


def fetch_emails(max_results=5):
    """Fetches recent emails, classifies with LLM, and applies labels."""
    service = load_gmail_service()
    processed_label_id = get_or_create_label("AI Processed")
    marketing_label_id = get_or_create_label(
        "Marketing"
    )  # Prepare 'Marketing' label too

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
                format="full",
                metadataHeaders=["Subject", "From"],
            )
            .execute()
        )

        # Skip if already labeled as processed
        if processed_label_id in msg_detail.get("labelIds", []):
            print(f"⚠️ Skipping already processed email ID: {msg_id}\n")
            continue

        headers = msg_detail.get("payload", {}).get("headers", [])
        subject = next(
            (h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)"
        )
        sender = next(
            (h["value"] for h in headers if h["name"] == "From"), "(Unknown Sender)"
        )

        # Extract plain text body (first part only, MVP)
        body = ""
        parts = msg_detail.get("payload", {}).get("parts", [])
        for part in parts:
            if part.get("mimeType") == "text/plain":
                body = part.get("body", {}).get("data", "")
                break

        print(f"📧 From: {sender}")
        print(f"   Subject: {subject}\n")

        # LLM Classification
        result = classify_email_with_llm(sender, subject, body)
        print(f"🤖 LLM Classification: {result}\n")

        # Build label list dynamically
        labels_to_add = [processed_label_id]  # Always apply "AI Processed"
        if result["category"] == "marketing":
            labels_to_add.append(marketing_label_id)  # Add "Marketing" if applicable

        # Apply labels
        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"addLabelIds": labels_to_add, "removeLabelIds": []},
        ).execute()

        print(f"✅ Applied labels to email ID: {msg_id}\n")


def move_to_marketing_folder(email_id):
    # Placeholder to move emails to marketing folder
    pass


def send_summary_email(summary):
    # Placeholder to send summary email via Gmail API
    pass
