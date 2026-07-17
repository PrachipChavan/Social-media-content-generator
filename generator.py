"""
generator.py — Groq API integration for content generation.
"""

import os
from groq import Groq
from dotenv import load_dotenv
from prompts import build_system_prompt, build_user_prompt

load_dotenv()


def get_groq_client(api_key: str) -> Groq:
    return Groq(api_key=api_key)


def generate_variations(
    api_key: str,
    platform: str,
    topic: str,
    tone: str,
    audience: str = "",
    keywords: str = "",
    num_variations: int = 3,
    model: str = "llama-3.3-70b-versatile",
) -> list[str]:
    """
    Generate multiple content variations for the given platform and topic.
    Returns a list of generated content strings.
    """
    client = get_groq_client(api_key)
    system_prompt = build_system_prompt()
    results = []

    for i in range(1, num_variations + 1):
        user_prompt = build_user_prompt(
            platform=platform,
            topic=topic,
            tone=tone,
            audience=audience,
            keywords=keywords,
            variation_num=i,
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.85,
            max_tokens=1024,
        )

        content = response.choices[0].message.content.strip()
        results.append(content)

    return results
