# Email Agent AI Microservice

This project is a fully automated AI-powered email agent designed to organize your Gmail inbox and keep your tasks under control. It runs continuously inside a Docker container.

## Features

- Automatically scans your Gmail inbox
- Detects and moves marketing emails to a separate folder
- Identifies questions or tasks in legitimate emails and creates To-Do items
- Sends daily summary reports via email, including:
  - Total emails received
  - Number of marketing emails
  - Number of legitimate emails
  - Number of To-Do items created

## How It Works

1. Connects to Gmail using OAuth2
2. Scans emails:
   - Detects marketing emails using unsubscribe links and keywords.
   - Extracts actionable tasks or questions using AI/NLP models.
3. Manages To-Do items locally.
4. Sends an end-of-day summary email.

## Technologies Used

- Gmail API
- Python (Requests, OAuthlib, etc.)
- AI/NLP via OpenAI or LangChain + spaCy
- SQLite (or JSON) for To-Do storage
- Docker (for easy deployment)
- Optional: FastAPI for health checks or web UI

## Running the Agent

```bash
docker build -t email-agent-ai .
docker run -d --env-file .env email-agent-ai
