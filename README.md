# 📰 Fake News Detector for Students

A Gradio-powered web app that summarizes any online news article and checks its credibility based on known, reliable news sources.

> 🔗 Built with [Gradio](https://www.gradio.app/) and [Hugging Face Transformers](https://huggingface.co/transformers/), powered by `distilbart-cnn-12-6`, `bert-tiny-finetuned-fake-news-detection`.

---

## 🚀 Demo

If deployed on [Hugging Face Spaces](https://huggingface.co/spaces), link it here:

👉 [Live Demo](https://huggingface.co/spaces/Rodu17/fake-news_detector)

---

## 🚀 Run it Instantly on Google Colab

> 📌 But first, insert this special code to install the required packages: # 🚀 Install dependencies
- !pip install gradio newspaper3k transformers lxml[html_clean] torch 

---

## 🚀 Run it Instantly on VS Code

> 📌 But first, insert this special code to install the required packages: # 🚀 Install dependencies
- !pip install gradio newspaper3k transformers lxml[html_clean] torch
- Run on local URL:  http://127.0.0.1:7860

---

Note - try to create a seperate environment
- python -m venv venv
- venv\Scripts\activate
- python app.py

---

## ✨ Features

- 🔒 Login feature
- ✅ Summarizes news articles from any URL
- 🔍 Verifies source credibility (BBC, NYTimes, AP, etc.)
- 📄 Optionally displays full article content
- ⚡ Runs entirely in your browser via Google Colab + Gradio
- 📄 Retains history

---

## 🧰 Tech Stack

- `gradio` – Web interface
- `newspaper3k` – Article extraction
- `transformers` – Text summarization using `distilbart-cnn-12-6`
- `lxml` – HTML parsing backend

---

## 🔗 Trusted Sources

The app checks the credibility of a news article based on whether its domain matches one of the following trusted news sources:

- bbc.com
- nytimes.com
- apnews.com
- indianexpress.com
- deccanherald.com

> You can customize this list by modifying the RELIABLE_SOURCES array in the app.py file:

