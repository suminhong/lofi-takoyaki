from dotenv import load_dotenv
load_dotenv(verbose=True)

import os, random
from moviepy import AudioFileClip, concatenate_audioclips

from utils.createimage import create_thumbnail
from utils.createmovie import create_movie_from_image
from utils.youtube import youtube_flow



## 여기만 바꿔가며 돌리기
working_path = "/Users/honglab/Desktop/lofi-takoyaki/20250221_1"
# title = "포근한 조명 아래, 친구들과 함께하는 따뜻한 순간 ☕🎶 | Cozy Dinner Lofi"
# moods = ["Dreamy", "Hopeful", "Relaxing", "Happy", "Sentimental", "Peaceful", "Smooth", "Restless", "Quirky", "Floating", "Romantic", "Dark", "Eccentric", "Heavy & Ponderous", "Funny", "Lounge", "Mysterious", "Sad", "Elegant"]



subjectfile_path = f"{working_path}/title.txt"
imagefile_path = f"{working_path}/1_init_image.webp"
videofile_path = f"{working_path}/2_video.mp4"
audiofile_path = f"{working_path}/3_sound.mp3"
finalfile_path = f"{working_path}/4_final.mov"
thumbnail_path = f"{working_path}/5_thumbnail.jpg"

# title = "조용한 아침, 따스한 나의 Lofi 이야기 🌅"

# [Dreamy, Hopeful, Relaxing, Happy, Sentimental, Peaceful, Smooth, Restless, Quirky, Floating, Romantic, Dark, Eccentric, Heavy & Ponderous, Funny, Lounge, Mysterious, Sad, Elegant]

# create_thumbnail(
#     f"{working_path}/1_init_image.webp",
#     f"{working_path}/5_thumbnail.jpg"
# )


# 음원 리스트가 미리 해당 경로에 저장되어 있는 경우
mp3_files = [AudioFileClip(os.path.join(working_path, f)) for f in os.listdir(working_path) if f.endswith(".mp3")]
random.shuffle(mp3_files)
audio_clip = concatenate_audioclips(mp3_files)
audio_clip.write_audiofile(audiofile_path)

# 썸네일이 없으면 생성
if not os.path.exists(thumbnail_path):
    create_thumbnail(imagefile_path, thumbnail_path)

create_movie_from_image(working_path)

youtube_flow(working_path)
