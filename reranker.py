import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def rerank(question: str, candidates: list):
    formatted = []
    for c in candidates:
        formatted.append(
            f"Tip {c['tip_number']}: {c['text'][:300]}"
        )

    prompt = f"""
You are selecting guidance for a parent of a child with autism.

Question:
"{question}"

Select up to 3 tips that BEST answer the question.
Prefer practical, step-by-step guidance.
Return ONLY a JSON array of tip_numbers.

Candidate tips:
{chr(10).join(formatted)}
"""

    resp = client.chat.completions.create(
        model="gpt-5.2",
        messages=[{"role": "system", "content": prompt}],
        temperature=0
    )

    return json.loads(resp.choices[0].message.content)
