import argparse, os, json, random, sys
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(verbose=True)

from utils import openai, pil, moviepy, selectmusic, youtube

WORKING_PATH = "/Users/honglab/Desktop/lofi-takoyaki"

SUBJECT_FILENAME = "subject.json"
IMAGE_WEBP_FILENAME = "image.webp"
IMAGE_JPG_FILENAME = "image.jpg"
IMAGE_VEDIO_FILENAME = "image_vedio.mp4"
THUMBNAIL_FILENAME = "thumbnail.jpg"
AUDIO_FILENAME = "audio.mp3"
FINAL_VEDIO_FILENAME = "final.mov"

music_genre_configs = {
    'lofi-hiphop': {
        'audio_path': os.path.join(WORKING_PATH, 'epidemicsound/lofi-hiphop-laidback'),
        'title_prefix': " | relax lo-fi hip hop",
        'tags': ["lofi", "lofihiphop", "music", "playlist", "warm", "work", "coding", "relaxing", "relax", "study", "calm", "coffee", "cozy", "chill"],
    },
    'acoustic': {
        'audio_path': os.path.join(WORKING_PATH, 'epidemicsound/acoustic'),
        'title_prefix': " | relax acoustic playlist",
        'tags': ["acoustic", "music", "playlist", "warm", "work", "coding", "relaxing", "relax", "study", "calm", "coffee", "cozy", "chill"],
    },
    'jpop': {
        'audio_path': os.path.join(WORKING_PATH, 'epidemicsound/jpop'),
        'title_prefix': " | j-pop playlist",
        'tags': ["jpop", "music", "playlist", "warm", "work", "coding", "study", "coffee", "cozy", "chill"],
    },
    'jrock': {
        'audio_path': os.path.join(WORKING_PATH, 'epidemicsound/jrock'),
        'title_prefix': " | jrock playlist",
        'tags': ["jrock", "music", "playlist", "warm", "work", "coding", "study", "coffee", "cozy", "chill"],
    },
    'piano': {
        'audio_path': os.path.join(WORKING_PATH, 'epidemicsound/piano'),
        'title_prefix': " | relax piano playlist",
        'tags': ["piano", "music", "playlist", "warm", "work", "coding", "relaxing", "relax", "study", "calm", "coffee", "cozy", "chill", "romantic"],
    },
}

def main(dir_name, genre, lang):
    # WORKING_PATH/working_dir 경로가 없으면 생성
    working_dir = os.path.join(WORKING_PATH, dir_name)
    os.makedirs(working_dir, exist_ok=True)

    subject_file = os.path.join(working_dir, SUBJECT_FILENAME)
    thumbnail_file = os.path.join(working_dir, THUMBNAIL_FILENAME)
    image_webp_file = os.path.join(working_dir, IMAGE_WEBP_FILENAME)
    image_jpg_file = os.path.join(working_dir, IMAGE_JPG_FILENAME)
    image_vedio_file = os.path.join(working_dir, IMAGE_VEDIO_FILENAME)
    audio_file = os.path.join(working_dir, AUDIO_FILENAME)
    final_file = os.path.join(working_dir, FINAL_VEDIO_FILENAME)
    
    # working_dir 안에 subject.json 파일이 있는지 확인
    if not os.path.exists(subject_file):
        subject_json = openai.create_subject_file(genre, lang, subject_file)
    else:
        with open(subject_file, "r") as f:
            subject_json = json.load(f)

    title = subject_json["title"]
    moods = subject_json["moods"]

    if not os.path.exists(thumbnail_file):
        if not os.path.exists(image_jpg_file):
            if not os.path.exists(image_webp_file):
                # dall-e 3: 이미지 생성
                openai.create_image_file(title, image_webp_file)
            
            # PIL: jpg이미지로 추가 저장
            pil.webp_to_jpg(image_webp_file, image_jpg_file)
        
        # PIL: 썸네일 생성
        pil.create_thumbnail(image_jpg_file, thumbnail_file)
    
    if not os.path.exists(final_file):
        if not os.path.exists(audio_file):
            audio_files = []
            # 작업 디렉토리 내의 모든 mp3 파일 찾기
            existing_mp3s = [os.path.join(working_dir, f) for f in os.listdir(working_dir) if f.endswith('.mp3') and f != AUDIO_FILENAME]
            if existing_mp3s:
                # 기존 mp3 파일들을 랜덤으로 선택
                random.shuffle(existing_mp3s)
                audio_files = existing_mp3s[:]
            else:
                audio_file_path = music_genre_configs[genre]['audio_path']
                selected_songs = selectmusic.filter_and_select_songs(os.listdir(audio_file_path), moods, num=20)
                audio_files = [f"{audio_file_path}/{song[2]}" for song in selected_songs]
            
            # audio_file 저장
            print(audio_files)
            moviepy.merge_mp3_files(audio_files, audio_file)
        
        if not os.path.exists(image_vedio_file):
            moviepy.image_to_video(image_jpg_file, image_vedio_file, moviepy.get_audio_duration(audio_file))
        
        # final_file 저장
        moviepy.merge_video_audio(image_vedio_file, audio_file, final_file)

    # title, thumbnail_file, final_file 확인 후 유튜브 업로드 플로우 진행
    youtube.youtube_upload(final_file, thumbnail_file, title, music_genre_configs[genre]['title_prefix'], music_genre_configs[genre]['tags'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='플레이리스트 영상 생성 및 유튜브 업로드 프로그램')
    parser.add_argument(
        "--dir", 
        type=str,
        default='',
        help="작업할 디렉토리 경로 (미지정시 타임스탬프로 생성됨)"
    )
    parser.add_argument(
        "--genre",
        type=str,
        choices=list(music_genre_configs.keys()),
        required=False,
        default='lofi-hiphop',
        help="생성할 음악 장르 선택"
    )
    parser.add_argument(
        "--lang",
        type=str,
        choices=['kr', 'en'],
        required=False,
        default='kr',
        help="제목 언어 선택"
    )
    parser.add_argument(
        "--auth",
        action="store_true",
        help="YouTube API 인증 플로우 실행"
    )
    args = parser.parse_args()

    if args.auth:
        print("YouTube API 인증을 시작합니다...")
        youtube.authenticate_youtube()
        print("인증이 완료되었습니다.")
        sys.exit(0)

    # args.dir가 ''면 타임스탬프로 생성
    if args.dir == '':
        args.dir = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    main(args.dir, args.genre, args.lang)
