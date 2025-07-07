"""
Main Orchestrator - Coordinates the email agent tasks.
"""

from app import gmail_service, email_classifier, task_extractor, todo_manager, reporter

def run_agent():
    # Authenticate with Gmail
    gmail_service.authenticate_gmail()

    # Fetch emails
    emails = gmail_service.fetch_emails()

    email_stats = {
        "total": len(emails),
        "marketing": 0,
        "legitimate": 0,
        "todos_created": 0
    }

    for email in emails:
        if email_classifier.is_marketing_email(email["content"]):
            gmail_service.move_to_marketing_folder(email["id"])
            email_stats["marketing"] += 1
        else:
            tasks = task_extractor.extract_tasks_from_email(email["content"])
            if tasks:
                for task in tasks:
                    todo_manager.save_todo_item(task["title"], task.get("due_date"))
                email_stats["todos_created"] += len(tasks)
            email_stats["legitimate"] += 1

    summary = reporter.generate_daily_summary(email_stats)
    gmail_service.send_summary_email(summary)

if __name__ == "__main__":
    run_agent()
