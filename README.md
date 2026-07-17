# ⚡ AI Social Media Content Generator

A premium Streamlit application that uses the **Groq API** (powered by LLaMA 3.3 70B and other LLaMA models) to generate platform-perfect social media content for Twitter/X, Instagram, LinkedIn, Facebook, and YouTube.

Features a sleek dark-mode glassmorphism UI, tone selection, variation generation, built-in hashtag extractors, and content history.

---

## ✨ Features

- **📱 Platform-Specific Formatting:** Tailored outputs matching platform characteristics:
  - **Twitter/X:** Concise tweets (<280 chars) with char counter and 3-5 hashtags.
  - **Instagram:** Captions with hooks, line breaks, emojis, and a heavy hashtag block (20-30 tags).
  - **LinkedIn:** Long-form posts with hooks, short paragraphs, story elements, and professional hashtags.
  - **Facebook:** Conversational posts with high-engagement calls to action.
  - **YouTube:** SEO-optimized titles, search-friendly descriptions, and metadata tags.
- **🎨 Multiple Tones:** Professional, Casual, Funny, Inspirational, and Educational.
- **⚡ 3 Variations At Once:** Generate 3 distinct versions for a single topic to compare.
- **📋 Copy & Regenerate:** Quick copy-to-clipboard buttons and individual variation regeneration.
- **🏷️ Hashtag Aggregator:** Automatically extracts unique hashtags across all variations into a copy-friendly text block.
- **📚 Local History:** Automatically saves generated content locally to `content_history.json` and loads it in the sidebar.

---

## 🛠️ Project Structure

```text
social-media-generator/
├── app.py                  # Main Streamlit UI & layout
├── generator.py            # Groq API client integration
├── history.py              # Local JSON history helper functions
├── prompts.py              # Platform-specific prompt structures
├── requirements.txt        # Package dependencies
└── .env.example            # Environment variable template
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher installed.
- A free **Groq API Key** (Get one at [console.groq.com](https://console.groq.com/)).

### Installation

1. **Clone the repository or download the files:**
   ```bash
   git clone <your-repository-url>
   cd social-media-generator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (Optional):**
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   Add your API key inside `.env`:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
   *Note: You can also paste your API key directly in the web UI sidebar.*

### Running the Application

Launch the Streamlit app:
```bash
streamlit run app.py
```

Open your browser to the local URL (usually `http://localhost:8501`).

---

## 📦 Dependencies

- `streamlit` - UI Framework
- `groq` - Official Groq SDK
- `python-dotenv` - Environment config loader
- `pyperclip` - Copy-to-clipboard functionality
