import gradio as gr
from newspaper import Article
from transformers import pipeline
import re
import datetime

# Load summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Load fake news classifier model (you can change to a better one if you want)
fake_news_detector = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-fake-news-detection")

# Trusted news sources
RELIABLE_SOURCES = ["bbc.com", "nytimes.com", "apnews.com", "indianexpress.com", "deccanherald.com"]

# Simple users (in-memory)
users = {
    "admin": "admin123",
    "guest": "guest",
    "user": "user"
}

# Session data store
user_sessions = {}

# Utility functions
def extract_domain(url):
    match = re.search(r"https?://(www\.)?([^/]+)", url)
    return match.group(2) if match else ""

def is_reliable_source(url):
    domain = extract_domain(url)
    return any(source in domain for source in RELIABLE_SOURCES)

def login(username, password):
    if users.get(username) == password:
        user_sessions[username] = {"history": []}
        return (f"✅ Logged in as {username}",
                gr.update(visible=True), gr.update(visible=False), username)
    return ("❌ Invalid credentials - please try again.",
            gr.update(visible=False), gr.update(visible=True), "")

def logout(username):
    user_sessions.pop(username, None)
    return "", gr.update(visible=False), gr.update(visible=True), ""

def analyze_article(url, username):
    if not url.startswith("http"):
        return "❌ Invalid URL", "", "", "", ""

    try:
        article = Article(url)
        article.download()
        article.parse()

        text = article.text.strip()
        if len(text) < 100:
            return "❌ Article too short to analyze", "", "", "", ""

        # Summarize article (limit input length for model)
        summary = summarizer(text[:1024], max_length=130, min_length=30, do_sample=False)[0]['summary_text']

        # Source credibility check
        credibility = "✅ Trusted Source" if is_reliable_source(url) else "⚠️ Unverified Source"

        # Fake news detection (on article text or summary)
        fake_pred = fake_news_detector(summary)[0]
        label = fake_pred['label']
        score = fake_pred['score']
        fake_news_status = ""
        if label == "FAKE":
            fake_news_status = f"🚨 Warning: This article is likely FAKE news (confidence: {score:.2f})"
        else:
            fake_news_status = f"✅ Article appears credible (confidence: {score:.2f})"

        # Save to user history
        if username in user_sessions:
            user_sessions[username]["history"].append({
                "url": url,
                "summary": summary,
                "credibility": credibility,
                "fake_news_status": fake_news_status,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        return "", summary, credibility, fake_news_status, text

    except Exception as e:
        return f"❌ Error analyzing article: {str(e)}", "", "", "", ""

def get_history(username):
    if username in user_sessions:
        history = user_sessions[username]["history"]
        if not history:
            return "No articles analyzed yet."
        return "\n\n".join(
            [f"[{item['timestamp']}]\n{item['url']}\nSummary: {item['summary'][:100]}...\nCredibility: {item['credibility']}\nStatus: {item['fake_news_status']}"
             for item in history]
        )
    return "User not found."

with gr.Blocks(title="📰 Fake News Detector for Students") as app:
    gr.Markdown("# 📰 Fake News Detector for Students")
    gr.Markdown("Paste an article URL to check its summary, source credibility, and likelihood of being fake news.")

    logged_in_user = gr.State("")

    with gr.Tab("🔐 Login"):
        login_user = gr.Textbox(label="Username")
        login_pass = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        login_msg = gr.Markdown()
        login_area = gr.Group(visible=True)
        app_area = gr.Group(visible=False)

    login_btn.click(login, inputs=[login_user, login_pass],
                    outputs=[login_msg, app_area, login_area, logged_in_user])

    with app_area:
        gr.Markdown("## 🔍 Analyze Article")

        url_input = gr.Textbox(label="Paste Article URL here")
        analyze_btn = gr.Button("Analyze")

        error_output = gr.Markdown()
        summary_output = gr.Textbox(label="📝 Summary", lines=4)
        credibility_output = gr.Textbox(label="🔍 Source Credibility", max_lines=1)
        fake_news_output = gr.Textbox(label="⚠️ Fake News Detection Result", max_lines=2)

        with gr.Accordion("📄 Full Article Text ", open=False):
            full_text_output = gr.Textbox(label="Full Article", lines=40, interactive=False)

        analyze_btn.click(analyze_article,
                          inputs=[url_input, logged_in_user],
                          outputs=[error_output, summary_output, credibility_output, fake_news_output, full_text_output])

        gr.Markdown("## 📜 Article History")
        history_output = gr.Textbox(label="Past Analyzed Articles", lines=8)
        history_btn = gr.Button("🔄 Refresh History")
        history_btn.click(get_history, inputs=logged_in_user, outputs=history_output)

        logout_btn = gr.Button("🚪 Logout")
        logout_btn.click(logout, inputs=logged_in_user,
                         outputs=[login_msg, app_area, login_area, logged_in_user])

app.launch()
