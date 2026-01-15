import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts import RESOURCE_COMPOSER_PROMPT, FALLBACK_PROMPT

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def build_context(chunks):
    return "\n\n---\n\n".join(
        f"Tip {c['tip_number']}:\n{c['text']}"
        for c in chunks
    )

def compose_answer(question: str, chunks: list):
    context = build_context(chunks)

    prompt = RESOURCE_COMPOSER_PROMPT.format(
        context=context,
        question=question
    )

    resp = client.chat.completions.create(
        model="gpt-5.2",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.2
    )

    return resp.choices[0].message.content.strip()

def fallback_answer(question: str):
    prompt = FALLBACK_PROMPT.format(question=question)

    resp = client.chat.completions.create(
        model="gpt-5.2",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.3
    )

    return resp.choices[0].message.content.strip()
