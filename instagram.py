import requests
import dropbox
import os
import time
from dotenv import load_dotenv

load_dotenv()

FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
IG_BUSINESS_ACCOUNT_ID = os.getenv("IG_BUSINESS_ACCOUNT_ID")
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

local_files_path = [
    "beauty_summary_in_en.mp4",
    "beauty_summary_in_es.mp4",
    "beauty_summary_in_pl.mp4",
    "beauty_summary_in_tr.mp4",
]
dropbox_files_path = [
    "/beauty_summary_in_en.mp4",
    "/beauty_summary_in_es.mp4",
    "/beauty_summary_in_pl.mp4",
    "/beauty_summary_in_tr.mp4",
]


def upload_to_dropbox(local_file_path, dropbox_file_path):
    try:
        with open(local_file_path, "rb") as f:
            dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode.overwrite)
        print(f"Uploaded {local_file_path} to Dropbox at {dropbox_file_path}")

        # Get or create a shared link
        shared_links = dbx.sharing_list_shared_links(path=dropbox_file_path).links
        shared_url = shared_links[0].url if shared_links else dbx.sharing_create_shared_link_with_settings(
            dropbox_file_path).url

        # Convert to a direct download URL
        return shared_url.replace("?dl=0", "?raw=1")

    except Exception as e:
        print(f"Error uploading to Dropbox: {e}")
        return None


def upload_story_to_instagram(video_url):
    try:
        upload_url = f"https://graph.facebook.com/v21.0/{IG_BUSINESS_ACCOUNT_ID}/media"
        params = {
            "media_type": "REELS",
            "video_url": video_url,
            "access_token": FACEBOOK_ACCESS_TOKEN,
        }
        response = requests.post(upload_url, data=params).json()

        if "id" not in response:
            print(f"Error during upload: {response}")
            return None

        creation_id = response["id"]

        # Poll for readiness
        while True:
            status_response = requests.get(
                f"https://graph.facebook.com/v21.0/{creation_id}",
                params={"access_token": FACEBOOK_ACCESS_TOKEN},
            ).json()

            if status_response.get("status") == "READY":
                publish_url = f"https://graph.facebook.com/v21.0/{IG_BUSINESS_ACCOUNT_ID}/media_publish"
                publish_response = requests.post(
                    publish_url,
                    data={"creation_id": creation_id, "access_token": FACEBOOK_ACCESS_TOKEN},
                ).json()
                return publish_response

            print("Media not ready, waiting...")
            time.sleep(30)

    except Exception as e:
        print(f"Error uploading story to Instagram: {e}")
        return None


def delete_from_dropbox(file_path):
    try:
        dbx.files_delete_v2(file_path)
        print(f"Deleted {file_path} from Dropbox.")
    except Exception as e:
        print(f"Error deleting file from Dropbox: {e}")


def process_and_upload_videos_instagram():
    for i, file_path in enumerate(local_files_path):
        dropbox_path = dropbox_files_path[i]


        video_url = upload_to_dropbox(file_path, dropbox_path)
        if video_url:
            print(f"Video uploaded to Dropbox. Direct link: {video_url}")


            instagram_response = upload_story_to_instagram(video_url)
            print(f"Instagram response: {instagram_response}")


            delete_from_dropbox(dropbox_path)
        else:
            print(f"Failed to upload {file_path} to Dropbox.")
