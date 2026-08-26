# Agents/database.py

import json
import sqlite3

from Agents.paths import (
    DATABASE_PATH,
    CONFIG_PATH,
    CSS_PATH,
    PROMPT_PATH,
    Userdetail_PATH
)


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def get_config():

    with open(
        CONFIG_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def get_style():

    with open(
        CSS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def get_prompt(prompt_name,**kwargs):
    with open(PROMPT_PATH,"r",encoding="utf-8") as file:
        prompts = json.load(file)

    prompt = prompts[prompt_name]
    return prompt.format(**kwargs)


def get_user_details():

    with open(Userdetail_PATH,"r",encoding="utf-8") as file:
        users = json.load(file)

    user = users["user_persona"]

    context = f"""
                Name: {user['name']}
                Role: {", ".join(user['role'])}
                Experience: {user['experience']}
                Domain: {user['domain']}
                Skills: {", ".join(user['skills'])}
                Career Goals: {", ".join(user['career_goals'])}
                """

    return context.strip()