from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth import credentials

def upload_video_to_google(video_path, video_name):
    #Credenciais
    creds = credentials.Credentials.from_authorized_user_file('credentials.json')
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    #Cria uma Instancia do Youtube
    youtube = build('youtube', 'v3', credentials=creds)
    media = MediaFileUpload(video_path)

    #VIDEO
    request = youtube.videos().insert(
        part='snippet',
        body={
            'snippet': {
                'title': video_name,
            },
            'status': {
                'privacyStatus': 'public'
            }
        },
        media_body=media
    )

    #Request do upload upload
    response = request.execute()
    print(response)
