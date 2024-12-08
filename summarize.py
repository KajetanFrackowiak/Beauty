from transformers import pipeline
from deep_translator import GoogleTranslator
from fetch_news import fetch_beauty_news

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_articles_together(articles, target_languages=None):
    combined_text = " ".join([f"{article.get('title', '')}: {article.get('content', '')}" for article in articles if article.get('content', '')])

    if not combined_text:
        return {"title": "No Title", "summary": "No content available to summarize.", "translated_summary": None}

    summary = summarizer(combined_text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]

    if target_languages:
        translator = GoogleTranslator(target=target_languages)
        summary = translator.translate(summary)

    title =  articles[0].get('title', 'No Title') if articles else "No Title"

    return {"title": title, "summary": summary}

def get_summaries():
    news = fetch_beauty_news()
    selected_articles = news[:5]
    medium_articles = selected_articles[:3]
    substack_articles = selected_articles[3:]

    medium_summary_en = summarize_articles_together(medium_articles)
    medium_summary_es = summarize_articles_together(medium_articles, target_languages="es")
    medium_summary_pl = summarize_articles_together(medium_articles, target_languages="pl")
    medium_summary_tr = summarize_articles_together(medium_articles, target_languages="tr")

    substack_summary_en = summarize_articles_together(substack_articles)
    substack_summary_es = summarize_articles_together(substack_articles, target_languages="es")
    substack_summary_pl = summarize_articles_together(substack_articles, target_languages="pl")
    substack_summary_tr = summarize_articles_together(substack_articles, target_languages="tr")

    all_summary_en = summarize_articles_together(selected_articles)
    all_summary_es = summarize_articles_together(selected_articles, target_languages="es")
    all_summary_pl = summarize_articles_together(selected_articles, target_languages="pl")
    all_summary_tr = summarize_articles_together(selected_articles, target_languages="tr")

    return {
        "medium": {
            "en": medium_summary_en,
            "es": medium_summary_es,
            "pl": medium_summary_pl,
            "tr": medium_summary_tr,
        },
        "substack": {
            "en": substack_summary_en,
            "es": substack_summary_es,
            "pl": substack_summary_pl,
            "tr": substack_summary_tr,
        },
        "all": {
            "en": all_summary_en,
            "es": all_summary_es,
            "pl": all_summary_pl,
            "tr": all_summary_tr,
        },
    }