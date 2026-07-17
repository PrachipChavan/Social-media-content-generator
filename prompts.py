"""
prompts.py — Platform-specific prompt templates for social media content generation.
"""

PLATFORM_SPECS = {
    "Twitter/X": {
        "icon": "🐦",
        "color": "#1DA1F2",
        "char_limit": 280,
        "hashtag_count": "3-5",
        "description": "Concise, punchy tweet under 280 characters",
    },
    "Instagram": {
        "icon": "📸",
        "color": "#E1306C",
        "char_limit": 2200,
        "hashtag_count": "20-30",
        "description": "Engaging caption with a heavy hashtag block",
    },
    "LinkedIn": {
        "icon": "💼",
        "color": "#0A66C2",
        "char_limit": 3000,
        "hashtag_count": "3-5",
        "description": "Professional long-form post with insights and a CTA",
    },
    "Facebook": {
        "icon": "👥",
        "color": "#1877F2",
        "char_limit": 63206,
        "hashtag_count": "3-5",
        "description": "Conversational post that encourages engagement",
    },
    "YouTube": {
        "icon": "▶️",
        "color": "#FF0000",
        "char_limit": 5000,
        "hashtag_count": "5-10",
        "description": "Video title + SEO-optimized description + tags",
    },
}

TONE_DESCRIPTIONS = {
    "Professional": "authoritative, polished, and formal — suitable for business audiences",
    "Casual": "friendly, relaxed, and conversational — like talking to a friend",
    "Funny": "witty, humorous, and playful — use puns, jokes, or clever observations",
    "Inspirational": "motivating, uplifting, and emotionally resonant — spark action",
    "Educational": "informative, clear, and structured — teach the audience something valuable",
}


def build_system_prompt() -> str:
    return (
        "You are an expert social media content strategist and copywriter with 10+ years of experience "
        "crafting viral content for top brands. You deeply understand platform algorithms, audience psychology, "
        "and what makes content shareable. You always produce content that feels authentic, native to the platform, "
        "and optimized for maximum engagement. You naturally incorporate relevant emojis to add personality and "
        "visual appeal without overdoing it."
    )


def build_user_prompt(
    platform: str,
    topic: str,
    tone: str,
    audience: str,
    keywords: str,
    variation_num: int,
) -> str:
    spec = PLATFORM_SPECS[platform]
    tone_desc = TONE_DESCRIPTIONS[tone]
    audience_line = f"Target audience: {audience}." if audience.strip() else ""
    keywords_line = f"Incorporate these keywords/themes: {keywords}." if keywords.strip() else ""

    platform_instructions = {
        "Twitter/X": f"""
Write a single tweet about the topic. Rules:
- STRICTLY under 280 characters (count carefully!)
- Include {spec['hashtag_count']} relevant hashtags
- Add 1-3 emojis naturally
- Make it punchy and scroll-stopping
- End with a hook or question to drive replies
- Variation #{variation_num}: Make this uniquely different from other variations
""",
        "Instagram": f"""
Write an Instagram caption. Rules:
- Start with a strong hook (first line visible before 'more')
- 150-300 words for the main caption body
- Use line breaks and emojis throughout
- End with a clear call-to-action (ask a question or encourage saves/shares)
- Add two blank lines then a block of {spec['hashtag_count']} highly relevant hashtags
- Variation #{variation_num}: Use a different angle or hook style
""",
        "LinkedIn": f"""
Write a LinkedIn post. Rules:
- Start with a bold, attention-grabbing first line (no fluff)
- 200-400 words with personal insight or data-backed points
- Use short paragraphs (1-2 sentences max)
- Include a personal story or professional lesson
- End with a thought-provoking question to drive comments
- Add {spec['hashtag_count']} professional hashtags at the end
- Variation #{variation_num}: Take a different professional angle
""",
        "Facebook": f"""
Write a Facebook post. Rules:
- Conversational and warm tone
- 100-200 words
- Include a question or poll suggestion to boost engagement
- Add 2-4 relevant emojis
- Include {spec['hashtag_count']} hashtags naturally within the text
- End with a clear call-to-action
- Variation #{variation_num}: Use a different engagement angle
""",
        "YouTube": f"""
Write YouTube video metadata. Format EXACTLY as:
**TITLE:** [Compelling, SEO-optimized title under 70 chars]

**DESCRIPTION:**
[First 2-3 sentences should hook the viewer and include the main keyword]
[Paragraphs explaining video content, timestamps section placeholder, links section]
[About 200-300 words total]

**TAGS:** [15-20 comma-separated tags]

Rules:
- Title should create curiosity or promise value
- Description first 150 chars are crucial for SEO
- Variation #{variation_num}: Try a different title style (e.g., How-To vs List vs Question)
""",
    }

    return f"""
Topic: {topic}
Platform: {platform} — {spec['description']}
Tone: {tone} ({tone_desc})
{audience_line}
{keywords_line}

{platform_instructions[platform]}

Generate ONLY the final content. No explanations, no labels, no meta-commentary.
""".strip()
