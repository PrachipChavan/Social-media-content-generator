"""
app.py — Main Streamlit UI for Social Media Content Generator.
"""

import streamlit as st
from generator import generate_variations
from history import load_history, save_to_history, delete_history_item, clear_history
from prompts import PLATFORM_SPECS, TONE_DESCRIPTIONS

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Social Media Content Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root & Body ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #0d0d1a 0%, #0f0f23 40%, #12102b 100%);
    min-height: 100vh;
}

/* ── Hide default Streamlit elements ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 1400px; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #6c2fe4 0%, #8b3dff 30%, #4f8cff 70%, #38d5ff 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(108, 47, 228, 0.4);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40%;
    left: 5%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 60%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.5px;
    position: relative;
    z-index: 1;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: rgba(255,255,255,0.85);
    margin: 0;
    font-weight: 400;
    position: relative;
    z-index: 1;
}

/* ── Glass Card ── */
.glass-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
.glass-card:hover {
    background: rgba(255, 255, 255, 0.07);
    border-color: rgba(139, 61, 255, 0.35);
    box-shadow: 0 8px 30px rgba(108, 47, 228, 0.2);
    transform: translateY(-2px);
}

/* ── Section Label ── */
.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #8b5cf6;
    margin-bottom: 0.4rem;
}

/* ── Platform Pill ── */
.platform-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1rem;
}
.platform-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    color: white;
    margin-bottom: 0.8rem;
}

/* ── Variation Card ── */
.variation-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    position: relative;
    transition: all 0.3s ease;
}
.variation-card:hover {
    border-color: rgba(139, 61, 255, 0.4);
    box-shadow: 0 4px 20px rgba(108, 47, 228, 0.15);
}
.variation-number {
    position: absolute;
    top: -12px;
    left: 20px;
    background: linear-gradient(135deg, #6c2fe4, #4f8cff);
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.2rem 0.7rem;
    border-radius: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.variation-content {
    color: #e2e8f0;
    font-size: 0.92rem;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
}
.char-count {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.35);
    margin-top: 0.8rem;
    text-align: right;
}
.char-count.over-limit {
    color: #f87171;
}

/* ── Divider ── */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,61,255,0.4), transparent);
    margin: 1.5rem 0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(13, 13, 30, 0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] .stMarkdown { color: #c4b5fd !important; }

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(139, 61, 255, 0.6) !important;
    box-shadow: 0 0 0 2px rgba(139, 61, 255, 0.15) !important;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ── Button styles ── */
.stButton > button {
    background: linear-gradient(135deg, #6c2fe4, #4f8cff) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(108, 47, 228, 0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(108, 47, 228, 0.5) !important;
}

/* ── Tone badge colors ── */
.tone-professional { color: #60a5fa; }
.tone-casual { color: #34d399; }
.tone-funny { color: #fbbf24; }
.tone-inspirational { color: #f472b6; }
.tone-educational { color: #a78bfa; }

/* ── History card ── */
.history-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    cursor: pointer;
    transition: all 0.2s ease;
}
.history-card:hover {
    background: rgba(139,61,255,0.08);
    border-color: rgba(139,61,255,0.3);
}
.history-meta {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.4);
    margin-top: 0.3rem;
}

/* ── Info boxes ── */
.info-box {
    background: rgba(79, 140, 255, 0.08);
    border: 1px solid rgba(79, 140, 255, 0.2);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    font-size: 0.83rem;
    color: #93c5fd;
    margin-bottom: 1rem;
}

/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.stat-chip {
    background: rgba(139,61,255,0.12);
    border: 1px solid rgba(139,61,255,0.2);
    border-radius: 8px;
    padding: 0.4rem 0.9rem;
    font-size: 0.78rem;
    color: #c4b5fd;
    font-weight: 500;
}

/* ── Spinner override ── */
.stSpinner > div { border-top-color: #8b3dff !important; }

/* ── Radio buttons ── */
.stRadio > div { flex-direction: row; flex-wrap: wrap; gap: 0.5rem; }
.stRadio label { color: #e2e8f0 !important; }

/* ── Label colors ── */
label, .stMarkdown p { color: #cbd5e1 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "generated_variations" not in st.session_state:
    st.session_state.generated_variations = []
if "current_platform" not in st.session_state:
    st.session_state.current_platform = ""
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""
if "current_tone" not in st.session_state:
    st.session_state.current_tone = ""
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "show_history_item" not in st.session_state:
    st.session_state.show_history_item = None


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem;'>
        <div style='font-size:2.2rem'>✨</div>
        <div style='font-size:1.1rem; font-weight:700; color:#c4b5fd;'>ContentAI</div>
        <div style='font-size:0.72rem; color:rgba(255,255,255,0.4); margin-top:0.2rem;'>Social Media Generator</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── API Key ──
    st.markdown("<div class='section-label'>🔑 Groq API Key</div>", unsafe_allow_html=True)
    api_key_input = st.text_input(
        label="api_key_field",
        value=st.session_state.api_key,
        type="password",
        placeholder="gsk_xxxxxxxxxxxxxxxx",
        label_visibility="collapsed",
    )
    if api_key_input:
        st.session_state.api_key = api_key_input

    st.markdown("""
    <div class='info-box'>
        🆓 Get your <b>free</b> API key at<br>
        <a href='https://console.groq.com' target='_blank' style='color:#93c5fd;'>console.groq.com</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── Model selector ──
    st.markdown("<div class='section-label'>🤖 Model</div>", unsafe_allow_html=True)
    model_choice = st.selectbox(
        "model_select",
        options=[
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── Content History ──
    st.markdown("<div class='section-label'>📚 Content History</div>", unsafe_allow_html=True)
    history = load_history()

    if not history:
        st.markdown("<div style='color:rgba(255,255,255,0.3); font-size:0.82rem; padding:0.5rem 0;'>No history yet. Generate some content!</div>", unsafe_allow_html=True)
    else:
        for item in history[:10]:
            platform_icon = PLATFORM_SPECS.get(item["platform"], {}).get("icon", "📄")
            col1, col2 = st.columns([5, 1])
            with col1:
                if st.button(
                    f"{platform_icon} {item['topic'][:28]}{'…' if len(item['topic']) > 28 else ''}",
                    key=f"hist_{item['id']}",
                    use_container_width=True,
                ):
                    st.session_state.show_history_item = item
                    st.session_state.generated_variations = item["variations"]
                    st.session_state.current_platform = item["platform"]
                    st.session_state.current_topic = item["topic"]
                    st.session_state.current_tone = item["tone"]
            with col2:
                if st.button("🗑", key=f"del_{item['id']}"):
                    delete_history_item(item["id"])
                    st.rerun()

        st.markdown("")
        if st.button("🗑️ Clear All History", use_container_width=True):
            clear_history()
            st.session_state.generated_variations = []
            st.rerun()


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────

# ── Hero Banner ──
st.markdown("""
<div class='hero-banner'>
    <div class='hero-title'>✨ Social Media Content Generator</div>
    <div class='hero-subtitle'>
        Craft platform-perfect content powered by LLaMA AI — in seconds.
        Twitter, Instagram, LinkedIn, Facebook & YouTube.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stats row ──
history_count = len(load_history())
st.markdown(f"""
<div class='stats-row'>
    <div class='stat-chip'>🤖 LLaMA 3.3 70B</div>
    <div class='stat-chip'>🌐 5 Platforms</div>
    <div class='stat-chip'>🎨 5 Tones</div>
    <div class='stat-chip'>📚 {history_count} Saved Posts</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INPUT FORM
# ─────────────────────────────────────────────
with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    # ── Platform Selector ──
    st.markdown("<div class='section-label'>📱 Choose Platform</div>", unsafe_allow_html=True)

    platform_cols = st.columns(5)
    platforms = list(PLATFORM_SPECS.keys())
    selected_platform = st.session_state.get("selected_platform", platforms[0])

    platform_icons = {p: PLATFORM_SPECS[p]["icon"] for p in platforms}
    selected_platform = st.radio(
        "platform_radio",
        options=platforms,
        format_func=lambda p: f"{platform_icons[p]} {p}",
        horizontal=True,
        label_visibility="collapsed",
    )

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── Topic + Tone row ──
    col_left, col_right = st.columns([3, 1])

    with col_left:
        st.markdown("<div class='section-label'>💡 Topic / Brief</div>", unsafe_allow_html=True)
        topic = st.text_area(
            "topic_input",
            placeholder="e.g. Announcing our new AI-powered fitness app that tracks workouts using your phone camera...",
            height=100,
            label_visibility="collapsed",
        )

    with col_right:
        st.markdown("<div class='section-label'>🎨 Tone</div>", unsafe_allow_html=True)
        tone = st.selectbox(
            "tone_select",
            options=list(TONE_DESCRIPTIONS.keys()),
            label_visibility="collapsed",
        )
        st.markdown(f"""
        <div style='font-size:0.75rem; color:rgba(255,255,255,0.4); margin-top:0.3rem; line-height:1.4;'>
            {TONE_DESCRIPTIONS[tone]}
        </div>
        """, unsafe_allow_html=True)

    # ── Optional fields ──
    with st.expander("⚙️ Advanced Options (optional)"):
        adv_col1, adv_col2 = st.columns(2)
        with adv_col1:
            audience = st.text_input(
                "Target Audience",
                placeholder="e.g. fitness enthusiasts aged 25-40",
                label_visibility="visible",
            )
        with adv_col2:
            keywords = st.text_input(
                "Keywords / Themes",
                placeholder="e.g. AI, fitness, health, technology",
                label_visibility="visible",
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Generate Button ──
    st.markdown("<br>", unsafe_allow_html=True)
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    with btn_col2:
        generate_clicked = st.button(
            "⚡ Generate Content  →",
            use_container_width=True,
            type="primary",
        )


# ─────────────────────────────────────────────
# GENERATION LOGIC
# ─────────────────────────────────────────────
if generate_clicked:
    if not st.session_state.api_key:
        st.error("🔑 Please enter your Groq API key in the sidebar first!")
    elif not topic.strip():
        st.warning("💡 Please enter a topic or brief before generating.")
    else:
        with st.spinner(f"🤖 Crafting 3 {selected_platform} variations for you..."):
            try:
                variations = generate_variations(
                    api_key=st.session_state.api_key,
                    platform=selected_platform,
                    topic=topic,
                    tone=tone,
                    audience=audience if "audience" in dir() else "",
                    keywords=keywords if "keywords" in dir() else "",
                    model=model_choice,
                )
                st.session_state.generated_variations = variations
                st.session_state.current_platform = selected_platform
                st.session_state.current_topic = topic
                st.session_state.current_tone = tone
                save_to_history(selected_platform, topic, tone, variations)
                st.rerun()
            except Exception as e:
                error_msg = str(e)
                if "401" in error_msg or "invalid_api_key" in error_msg.lower():
                    st.error("🔑 Invalid API key. Please check your Groq API key.")
                elif "rate_limit" in error_msg.lower():
                    st.error("⏳ Rate limit reached. Please wait a moment and try again.")
                else:
                    st.error(f"❌ Generation failed: {error_msg}")


# ─────────────────────────────────────────────
# RESULTS DISPLAY
# ─────────────────────────────────────────────
if st.session_state.generated_variations:
    platform = st.session_state.current_platform
    topic_display = st.session_state.current_topic
    tone_display = st.session_state.current_tone
    spec = PLATFORM_SPECS.get(platform, {})
    char_limit = spec.get("char_limit", 9999)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── Results header ──
    st.markdown(f"""
    <div style='display:flex; align-items:center; gap:1rem; margin-bottom:1.5rem;'>
        <span style='font-size:1.6rem'>{spec.get('icon','📄')}</span>
        <div>
            <div style='font-size:1.2rem; font-weight:700; color:#e2e8f0;'>
                {platform} Content
            </div>
            <div style='font-size:0.8rem; color:rgba(255,255,255,0.45);'>
                Topic: <em>{topic_display[:60]}{'…' if len(topic_display)>60 else ''}</em>
                &nbsp;·&nbsp; Tone: <b>{tone_display}</b>
                &nbsp;·&nbsp; {len(st.session_state.generated_variations)} variations
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 3 Variation Cards ──
    for i, content in enumerate(st.session_state.generated_variations, 1):
        char_count = len(content)
        is_twitter = platform == "Twitter/X"
        over_limit = is_twitter and char_count > 280

        st.markdown(f"""
        <div class='variation-card'>
            <div class='variation-number'>✦ Variation {i}</div>
            <div class='variation-content'>{content}</div>
            <div class='char-count {"over-limit" if over_limit else ""}'>
                {char_count:,} characters{f" / 280 limit ⚠️" if is_twitter else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Action buttons ──
        btn1, btn2, btn3, _ = st.columns([1.5, 1.5, 1.5, 3])

        with btn1:
            if st.button(f"📋 Copy V{i}", key=f"copy_{i}"):
                st.session_state[f"copied_{i}"] = content
                st.toast(f"✅ Variation {i} copied to clipboard!", icon="📋")

        with btn2:
            if st.button(f"⭐ Save V{i}", key=f"save_{i}"):
                st.toast(f"✅ Variation {i} already saved in history!", icon="⭐")

        with btn3:
            if st.button(f"🔄 Regenerate V{i}", key=f"regen_{i}"):
                if not st.session_state.api_key:
                    st.error("API key required!")
                else:
                    with st.spinner(f"Regenerating variation {i}..."):
                        try:
                            from generator import generate_variations as gen
                            new_var = gen(
                                api_key=st.session_state.api_key,
                                platform=platform,
                                topic=topic_display,
                                tone=tone_display,
                                model=model_choice,
                                num_variations=1,
                            )
                            st.session_state.generated_variations[i - 1] = new_var[0]
                            st.rerun()
                        except Exception as e:
                            st.error(f"Regeneration failed: {e}")

        # Show copied content in a text area for manual copy if needed
        if st.session_state.get(f"copied_{i}"):
            st.text_area(
                f"📋 Copy the text below (Ctrl+A, Ctrl+C):",
                value=st.session_state[f"copied_{i}"],
                height=120,
                key=f"copy_area_{i}",
            )

    # ── Hashtag extractor ──
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>🏷️ Hashtags from All Variations</div>", unsafe_allow_html=True)

    all_text = " ".join(st.session_state.generated_variations)
    import re
    hashtags = list(dict.fromkeys(re.findall(r"#\w+", all_text)))

    if hashtags:
        st.markdown(f"""
        <div class='glass-card'>
            <div style='display:flex; flex-wrap:wrap; gap:0.5rem;'>
                {"".join(
                    f"<span style='background:rgba(139,61,255,0.18); border:1px solid rgba(139,61,255,0.3); "
                    f"border-radius:6px; padding:0.2rem 0.6rem; font-size:0.8rem; color:#c4b5fd;'>{ht}</span>"
                    for ht in hashtags
                )}
            </div>
        </div>
        """, unsafe_allow_html=True)

        hashtag_str = " ".join(hashtags)
        hcol1, hcol2 = st.columns([3, 1])
        with hcol1:
            st.text_input("All hashtags (copy-friendly)", value=hashtag_str, label_visibility="collapsed")

    # ── Generate again ──
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡ Generate New Variations", use_container_width=False):
        st.session_state.generated_variations = []
        st.rerun()


# ─────────────────────────────────────────────
# EMPTY STATE
# ─────────────────────────────────────────────
else:
    st.markdown("""
    <div style='text-align:center; padding:4rem 2rem;'>
        <div style='font-size:4rem; margin-bottom:1rem;'>🚀</div>
        <div style='font-size:1.3rem; font-weight:600; color:#c4b5fd; margin-bottom:0.5rem;'>
            Ready to create viral content?
        </div>
        <div style='font-size:0.9rem; color:rgba(255,255,255,0.4); max-width:420px; margin:0 auto;'>
            Enter your topic above, choose your platform and tone, hit <b>Generate</b> — 
            and get 3 tailored variations instantly.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Platform feature cards ──
    st.markdown("<div class='section-label' style='text-align:center;'>Supported Platforms</div>", unsafe_allow_html=True)
    pcols = st.columns(5)
    for col, (pname, pspec) in zip(pcols, PLATFORM_SPECS.items()):
        with col:
            st.markdown(f"""
            <div class='glass-card' style='text-align:center; padding:1.2rem 0.8rem;'>
                <div style='font-size:2rem;'>{pspec['icon']}</div>
                <div style='font-weight:600; color:#e2e8f0; font-size:0.85rem; margin-top:0.4rem;'>{pname}</div>
                <div style='font-size:0.7rem; color:rgba(255,255,255,0.4); margin-top:0.3rem;'>
                    {pspec['hashtag_count']} hashtags
                </div>
            </div>
            """, unsafe_allow_html=True)
