import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Agents.review_generator import get_weekly_summary
from Agents.ai_helper import ask_ai

weekly_data = get_weekly_summary()

prompt = f"""
You are my personal career coach.

Analyze the following activities:

{weekly_data}

Provide:

1. Achievements
2. Learning Summary
3. Challenges
4. Areas for Improvement
5. Next Week Goals
"""

review = ask_ai(prompt)

print(review)