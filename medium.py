import os
import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()

MEDIUM_API_KEY = os.getenv("MEDIUM_API_KEY")

def get_medium_user_id():
    headers = {
        "Authorization": f"Bearer {MEDIUM_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get("https://api.medium.com/v1/me", headers=headers)
    response_data = response.json()
    if response.status_code == 200:
        return response_data['data']['id']
    else:
        raise Exception(f"Error fetching user ID: {response_data}")

def post_to_medium(summary, title, language):
    user_id = get_medium_user_id()
    url = f"https://api.medium.com/v1/users/{user_id}/posts"
    headers = {
        "Authorization": f"Bearer {MEDIUM_API_KEY}",
        "Content-Type": "application/json"
    }

    translated_title = GoogleTranslator(source="auto", target=language).translate(title)

    data = {
        "title": translated_title,
        "contentFormat": "html",
        "content": f"<h2>{summary}</h2><p>",
        "tags": ["Beauty", "News"],
        "publishStatus": "draft"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 429:
        raise Exception("Rate limit exceeded. Please try again later.")
    elif response.status_code not in [200, 201]:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        raise Exception(f"Invalid JSON response: {response.text}")

def read_summaries_from_file(filename):
    summaries = []
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read().strip().split("\n\n")
        for entry in content:
            lines = entry.split("\n")
            title = lines[0].replace("Title: ", "")
            summary = lines[1].replace("Summary: ", "")
            summaries.append({"Title": title, "Summary": summary})
    return summaries

def post_from_summary_medium():
    summaries_en = read_summaries_from_file("medium_summaries_en.txt")
    summaries_es = read_summaries_from_file("medium_summaries_es.txt")
    summaries_pl = read_summaries_from_file("medium_summaries_pl.txt")
    summaries_tr = read_summaries_from_file("medium_summaries_tr.txt")

    for summary in summaries_en:
        post_to_medium(summary["Summary"], summary["Title"], "en")
    for summary in summaries_es:
        post_to_medium(summary["Summary"], summary["Title"], "es")
    for summary in summaries_pl:
        post_to_medium(summary["Summary"], summary["Title"], "pl")
    for summary in summaries_tr:
        post_to_medium(summary["Summary"], summary["Title"], "tr")