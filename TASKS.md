
# Project Tasks - Email Agent AI Microservice

## 📋 User Story
As a busy user, I want an AI-powered email agent that organizes my Gmail inbox automatically, so that I can focus on important tasks and avoid email clutter.

## ✅ Acceptance Criteria
- The agent runs continuously inside a Docker container.
- On first run:
  - Connects to Gmail via OAuth.
  - Scans inbox emails.
  - Detects marketing emails (via unsubscribe links).
  - Moves them to a “Marketing” folder (creating it if necessary).
- For remaining emails:
  - Identifies tasks/questions using Ollama API.
  - Creates a To-Do item (title + optional deadline).
- Every day:
  - Sends a summary email reporting:
    - Total emails received.
    - Number of marketing emails.
    - Number of legitimate emails.
    - Number of to-dos created.

## 🚀 Task Breakdown
| Task # | Description                                                           | Priority | Dependency           | Status |
|--------|------------------------------------------------------------------------|----------|----------------------|--------|
| 1      | Set up OAuth2 Gmail connection and token handling                      | High     | None                 | Done    |
| 2      | Fetch inbox emails via Gmail API                                       | High     | Task 1               |        |
| 3      | Detect marketing emails (look for unsubscribe links, keywords)         | High     | Task 2               |        |
| 4      | Move marketing emails to “Marketing” folder (create if needed)         | High     | Task 3               |        |
| 5      | Extract tasks/questions from email body using Ollama API               | High     | Task 2               |        |
| 6      | Store To-Do items locally (JSON or SQLite)                             | Medium   | Task 5               |        |
| 7      | Generate daily email summary                                           | Medium   | Tasks 2, 3, 5, 6     |        |
| 8      | Send summary email via Gmail API                                       | Medium   | Task 7               |        |
| 9      | Automate daily run (via cron or scheduler)                             | Medium   | Tasks 7, 8           |        |
| 10     | Dockerize the app with `.env` config support                           | High     | Tasks 1-9 (for prod) |        |

## 📝 Development Plan
1. Build local proof-of-concept covering core email flow (Tasks 1-6).
2. Integrate Ollama API task extraction.
3. Implement daily reporting and summary email (Tasks 7-8).
4. Containerize app and configure for deployment (Tasks 9-10).
5. Review, test, and iterate.

---

This document is tracked in the repo to guide development milestones.
