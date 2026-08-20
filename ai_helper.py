# ai_helper.py

import os
import requests
import logging as log

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
AI_MODEL = os.getenv("OPENROUTER_AI_MODEL")
API_URL = os.getenv("OPENROUTER_URL")

if not API_KEY:
    log.error("OPENROUTER_API_KEY is missing! Check the .env file.")
else:
    log.info("OPENROUTER_API_KEY loaded successfully.")

def ask_ai(prompt):

    try:

        if not API_URL:
            log.error("OPENROUTER_URL is missing.")
            return "OPENROUTER_URL is missing."

        if not AI_MODEL:
            log.error("OPENROUTER_AI_MODEL is missing.")
            return "OPENROUTER_AI_MODEL is missing."

        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": AI_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        data = response.json()

        if "choices" not in data:
            log.error("OpenRouter Error Response: %s", data)
            return f"OpenRouter Error: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as ex:

        log.error("OPENROUTER CONFIG ISSUE: %s", ex)

        return f"Error: {ex}"
