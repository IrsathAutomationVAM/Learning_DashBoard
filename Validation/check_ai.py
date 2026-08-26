# test_ai.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Agents.ai_helper import ask_ai

response = ask_ai("Say hello in one sentence")

print(response)