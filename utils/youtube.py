import os, json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import googleapiclient.discovery
import googleapiclient.errors


SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

def authenticate_youtube():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds

def upload_video(video_file, title, description, tags, category_id, privacy_status):
    creds = authenticate_youtube()
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy_status,  # "public", "private", or "unlisted"
            "selfDeclaredMadeForKids": False,  # 아동용 영상 아님
        },
    }

    media_file = googleapiclient.http.MediaFileUpload(video_file, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    response = request.execute()
    print(f"Upload Successful: https://www.youtube.com/watch?v={response['id']}")

    return response['id']

def upload_thumbnail(video_id, thumbnail_path):
    creds = authenticate_youtube()
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=googleapiclient.http.MediaFileUpload(thumbnail_path)
    )

    response = request.execute()
    print("Thumbnail uploaded successfully!")

def add_video_to_playlist(video_id, playlist_id):
    creds = authenticate_youtube()
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    request_body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
    }

    request = youtube.playlistItems().insert(
        part="snippet",
        body=request_body
    )

    response = request.execute()
    print(f"Video added to playlist: {playlist_id}")

def youtube_upload(video_file, thumbnail_file, title, title_prefix, tags):
    
    try:
        authenticate_youtube()
        video_id = upload_video(
            video_file=video_file,
            title=title + title_prefix,
            description=" ".join([f"#{tag}" for tag in tags]),
            tags=tags,
            category_id="10",  # 10 - 음악
            privacy_status="public"
        )

        upload_thumbnail(video_id, thumbnail_file)
        playlist_id = "PLu0aa78J7p70qFYPZdEEJRtLbWmuG47ZP"  # 사용하려는 재생목록 ID 입력
        add_video_to_playlist(video_id, playlist_id)
    
        return True

    except Exception as e:
        print(f"youtube_upload 에서 문제 발생 : {e}")
        return False
