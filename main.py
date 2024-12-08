import os
import datetime

from instagram import  process_and_upload_videos_instagram
from substack import post_from_summary_substack, read_summary_from_file
from summarize import get_summaries
from tiktok import upload_files_on_tiktok
from video_creator import create_video_summary
from medium import post_from_summary_medium, read_summaries_from_file
from youtube import  process_and_upload_videos_youtube

def save_articles_to_file(filename, summaries):
    with open(filename, "w", encoding='utf-8') as f:
        if isinstance(summaries, list):
            for summary in summaries:
                f.write(f"Title: {summary.get('title', 'No Title')}\n")
                f.write(f"Summary: {summary.get('summary', 'No Summary')}\n\n")
        else:
            f.write(f"Title: {summaries.get('title', 'No Title')}\n")
            f.write(f"Summary: {summaries.get('summary', 'No Summary')}\n")



def main():
    summaries = get_summaries()

    save_articles_to_file("all_summaries_en.txt", summaries["all"]["en"])
    save_articles_to_file("all_summaries_es.txt", summaries["all"]["es"])
    save_articles_to_file("all_summaries_pl.txt", summaries["all"]["pl"])
    save_articles_to_file("all_summaries_tr.txt", summaries["all"]["tr"])

    save_articles_to_file("medium_summaries_en.txt", summaries["medium"]["en"])
    save_articles_to_file("medium_summaries_es.txt", summaries["medium"]["es"])
    save_articles_to_file("medium_summaries_pl.txt", summaries["medium"]["pl"])
    save_articles_to_file("medium_summaries_tr.txt", summaries["medium"]["tr"])

    save_articles_to_file("substack_summaries_en.txt", summaries["substack"]["en"])
    save_articles_to_file("substack_summaries_es.txt", summaries["substack"]["es"])
    save_articles_to_file("substack_summaries_pl.txt", summaries["substack"]["pl"])
    save_articles_to_file("substack_summaries_tr.txt", summaries["substack"]["tr"])


    post_from_summary_medium()
    post_from_summary_substack()

    summary_en = read_summary_from_file("all_summaries_en.txt")
    summary_es = read_summary_from_file("all_summaries_es.txt")
    summary_pl = read_summary_from_file("all_summaries_pl.txt")
    summary_tr = read_summary_from_file("all_summaries_tr.txt")

    create_video_summary(summary_en,  language="en")
    create_video_summary(summary_es, language="es")
    create_video_summary(summary_pl, language="pl")
    create_video_summary(summary_tr, language="tr")

    process_and_upload_videos_youtube()
    upload_files_on_tiktok()
    process_and_upload_videos_instagram()
    files_to_delete = [
        "all_summaries_en.txt",
        "all_summaries_es.txt",
        "all_summaries_pl.txt",
        "all_summaries_tr.txt",
        "beauty_summary_in_en.mp4",
        "beauty_summary_in_es.mp4",
        "beauty_summary_in_pl.mp4",
        "beauty_summary_in_tr.mp4",
        "medium_summaries_en.txt",
        "medium_summaries_es.txt",
        "medium_summaries_pl.txt",
        "medium_summaries_tr.txt",
        "substack_summaries_en.txt",
        "substack_summaries_es.txt",
        "substack_summaries_pl.txt",
        "substack_summaries_tr.txt"
    ]


    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"Deleted: {file}")
        else:
            print(f"File not found: {file}")


if __name__ == "__main__":
    main()