import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Code Reviewer",
    page_icon="🖥️",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

.stApp {
    background-color: #0A0A16;
    background-image:
        linear-gradient(rgba(139,92,246,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56,189,248,0.06) 1px, transparent 1px),
        radial-gradient(circle at 10% 0%, rgba(139,92,246,0.18), transparent 35%),
        radial-gradient(circle at 100% 30%, rgba(56,189,248,0.14), transparent 40%);
    background-size: 32px 32px, 32px 32px, 100% 100%, 100% 100%;
    box-shadow: inset 0 0 70px rgba(139,92,246,0.25), inset 0 0 130px rgba(56,189,248,0.15);
}

section[data-testid="stSidebar"] {
    background-color: #0D0D1A;
    border-right: 1px solid #262640;
    box-shadow: inset -8px 0 30px rgba(139,92,246,0.08);
}
section[data-testid="stSidebar"] h3 {
    color: #ECEDF7;
}

.app-title {
    font-size: 4rem !important;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 0.25rem;
    background: linear-gradient(90deg, #A78BFA, #38BDF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 40px rgba(139,92,246,0.4);
    display: inline-block;
    line-height: 1.1;
}
.app-subtitle {
    color: #8A8FA8;
    font-size: 1rem;
    margin-bottom: 0.6rem;
}
.title-rule {
    height: 2px;
    width: 64px;
    background: linear-gradient(90deg, #A78BFA, #38BDF8);
    margin-bottom: 1.8rem;
    border-radius: 2px;
    box-shadow: 0 0 8px rgba(139,92,246,0.6);
}

.section-label {
    color: #A0A5C0;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    margin: 1.5rem 0 0.4rem 0;
}
.label-rule {
    height: 2px;
    width: 40px;
    background: linear-gradient(90deg, #A78BFA, #38BDF8);
    margin-bottom: 0.6rem;
    border-radius: 2px;
    box-shadow: 0 0 8px rgba(139,92,246,0.6);
}

textarea, .stTextArea textarea {
    background-color: #12121F !important;
    color: #ECEDF7 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    border: 1px solid #302B55 !important;
    border-radius: 10px !important;
    line-height: 1.5 !important;
}
textarea:focus {
    border: 1px solid #A78BFA !important;
    box-shadow: 0 0 0 1px #A78BFA, 0 0 20px rgba(139,92,246,0.35) !important;
}

div[data-baseweb="select"] > div {
    background-color: #12121F !important;
    border: 1px solid #302B55 !important;
    border-radius: 10px !important;
}

div.stButton > button {
    background: linear-gradient(90deg, #7C3AED, #0EA5E9);
    color: #ffffff;
    border: none;
    padding: 0.6rem 2rem;
    border-radius: 10px;
    font-weight: 600;
    box-shadow: 0 0 20px rgba(124,58,237,0.4), 0 0 20px rgba(14,165,233,0.25);
}
div.stButton > button:hover {
    box-shadow: 0 0 30px rgba(124,58,237,0.6), 0 0 30px rgba(14,165,233,0.4);
    transform: translateY(-1px);
}

.review-panel {
    background-color: #12121F;
    border: 1px solid #302B55;
    border-left: 3px solid #A78BFA;
    border-radius: 10px;
    padding: 1.1rem 1.4rem;
    margin-top: 0.6rem;
    color: #D8DAEE;
    font-size: 1rem;
    line-height: 1.65;
    box-shadow: 0 0 24px rgba(139,92,246,0.1);
}
.review-panel code {
    background-color: #1B1B2E;
    padding: 0.15rem 0.35rem;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    color: #7DD3FC;
}
.status-idle {
    color: #55597A;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    margin-top: 0.6rem;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### How it works")
    st.write("Paste your code, pick a language, and run a review. Feedback appears below, powered by a live AI model.")
    st.divider()
    st.caption("Streamlit · Groq API · gpt-oss-120b")

st.markdown('<p class="app-title">Code.Reviewer</p>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Paste your code below and get a short, plain-language review.</p>', unsafe_allow_html=True)
st.markdown('<div class="title-rule"></div>', unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.markdown('<p class="section-label">Language</p><div class="label-rule"></div>', unsafe_allow_html=True)
language = st.selectbox("Language", ["Python", "JavaScript", "Java", "C++", "Other"], label_visibility="collapsed")

st.markdown('<p class="section-label">Your code</p><div class="label-rule"></div>', unsafe_allow_html=True)
code_input = st.text_area("Code", height=260, placeholder="def hello():\n    print('Hello world')", label_visibility="collapsed")

review_clicked = st.button("Run Review")

st.markdown('<p class="section-label">Review</p><div class="label-rule"></div>', unsafe_allow_html=True)

if review_clicked:
    if code_input.strip() == "":
        st.warning("Paste some code first.")
    else:
        with st.spinner("Reviewing..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"You are a code reviewer. The following code is written in {language}. "
                            "Write a short, plain-language review in 3-5 sentences or short bullet points. "
                            "Do not use headers, bold text, or numbered sections. Be direct and concise, "
                            "focusing only on the most important 2-3 points.\n\n"
                            f"{code_input}"
                        )
                    }
                ]
            )
            review = response.choices[0].message.content
            st.markdown(f'<div class="review-panel">{review}</div>', unsafe_allow_html=True)
else:
    st.markdown('<p class="status-idle">Waiting for input...</p>', unsafe_allow_html=True)