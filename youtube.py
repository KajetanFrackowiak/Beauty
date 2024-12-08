import os
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

# Set up the Youtube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube"]
CLIENT_SECRETS_FILE = "credential_key.json"

def get_authenticated_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

def upload_video(youtube, video_file, title, description, tags, category_id, privacy_status):
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
    print("Uploaded Complete!")

    video_id = response.get("id")
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"Video URL: {video_url}")
    return response

def process_and_upload_videos_youtube():
    youtube = get_authenticated_service()
    languages = ["en", "es", "pl", "tr"]
    original_title = "Beauty News Summary"
    original_description = "This is a summary of the beauty news articles."
    original_tags = ["Beauty", "News"]

    for language in languages:
        video_file = f"beauty_summary_in_{language}.mp4"
        title = GoogleTranslator(source="auto", target=language).translate(original_title)
        description = GoogleTranslator(source="auto", target=language).translate(original_description)
        tags = [GoogleTranslator(source="auto", target=language).translate(tag) for tag in original_tags]
        category_id = "22"
        privacy_status = "public"

        print(f"Uploading video: {video_file} in {language}")
        upload_video(youtube, video_file, title, description, tags, category_id, privacy_status)


