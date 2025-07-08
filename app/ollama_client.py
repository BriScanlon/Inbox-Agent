import requests
import json
import re

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Default Ollama API URL
OLLAMA_MODEL = "qwen3:8b"  # Change this to your preferred model if needed


def classify_email_with_llm(sender, subject, body):
    """Sends email data to Ollama LLM and returns category + confidence."""

    prompt = f"""
You are an email classification assistant.

Your task is to classify an email as either:
- "marketing"
- "not marketing"

Also provide a confidence score between 0 and 1:
- 1 means very confident.
- 0 means not confident.

Respond **only** in the following strict JSON format:
{{
  "category": "<marketing|not marketing>",
  "confidence": <float between 0 and 1>
}}

Here is the email:
Sender: {sender}
Subject: {subject}
Body:
{body}
"""

    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_API_URL, json=payload)
    if response.status_code == 200:
        result_text = response.json()["response"]
        try:
            # Extract last JSON object from text
            json_matches = re.findall(r"\{.*?\}", result_text, flags=re.DOTALL)
            if json_matches:
                result = json.loads(json_matches[-1])
                category = result.get("category", "unknown")
                confidence = result.get("confidence", 0.0)
                return {"category": category, "confidence": confidence}
            else:
                raise ValueError("No JSON found in response.")
        except Exception as e:
            print("⚠️ Failed to parse JSON from LLM response.")
            print("LLM Output:", result_text)
            print("Error:", e)
            return {"category": "unknown", "confidence": 0.0}
    else:
        print("❌ Ollama API request failed.")
        print("Status:", response.status_code)
        print("Response:", response.text)
        return {"category": "unknown", "confidence": 0.0}
