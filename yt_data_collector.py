import csv
import isodate
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Substitua YOUR_API_KEY pela sua chave de API
API_KEY = ''
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Abra o arquivo de canais e comece a coleta
with open('channels.txt', 'r') as channels_file:
    channel_ids = channels_file.read().strip().split("\n")

    with open('videos.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Título do vídeo", "Quantidade de Likes", "Quantidade de Visualizações", "Data de publicação do vídeo"])

        # Data de 15 dias atrás
        start_time = datetime.utcnow() - timedelta(days=90)
        start_time_str = start_time.isoformat("T") + "Z"

        for channel_id in channel_ids:
            # Pegue os vídeos do canal
            channel_response = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                order="date",
                publishedAfter=start_time_str,
                type="video",
                maxResults=15
            ).execute()

            for item in channel_response['items']:
                video_id = item['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                # Pegue os detalhes do vídeo
                video_response = youtube.videos().list(
                    part="snippet,statistics,contentDetails", # Inclua contentDetails aqui
                    id=video_id
                ).execute()

                video = video_response['items'][0]
                title = video['snippet']['title']
                likes = video['statistics']['likeCount']
                views = video['statistics']['viewCount']
                published_date = video['snippet']['publishedAt']
                duration = video['contentDetails']['duration']

                # Converta a duração em segundos para comparar
                duration_seconds = int(isodate.parse_duration(duration).total_seconds())

                # Verifique se o vídeo é um Short (menos de 60 segundos)
                if duration_seconds >= 60:
                    # Adicione a URL à linha do CSV
                    writer.writerow([title, likes, views, published_date])

print("Coleta concluída! Verifique o arquivo 'videos.csv'.")
