import random
import re

def parse_filename(filename):
    """
    파일명을 파싱하여 Mood, BPM, 제목을 추출하는 함수
    """
    match = re.match(r"([A-Za-z]+)_(\d+)_\d+-\d+__(.+)\.mp3", filename)
    if match:
        mood, bpm, title = match.groups()
        return mood, int(bpm), title, filename
    return None

def filter_and_select_songs(file_list, mood_list, num=30):
    """
    특정 Mood에 해당하는 곡 중 BPM 평균에서 ±8 이내로 30곡을 선택하는 함수
    """
    # 파일명을 파싱하여 Mood, BPM을 추출
    songs = [parse_filename(f) for f in file_list if parse_filename(f)]
    
    # 주어진 Mood 리스트에 포함된 곡만 필터링
    filtered_songs = [(mood, bpm, filename) for mood, bpm, title, filename in songs if mood in mood_list]
    all_songs = [(mood, bpm, filename) for mood, bpm, title, filename in songs]

    # Mood에 맞는 곡이 30개 이상이면 랜덤 선택
    if len(filtered_songs) >= num:
        selected_songs = random.sample(filtered_songs, num)
    else:
        selected_songs = filtered_songs.copy()  # 가능한 만큼 우선 선택

    while True:
        # 현재 선택된 곡들의 BPM 평균 계산
        bpm_values = [bpm for _, bpm, _ in selected_songs]
        bpm_avg = sum(bpm_values) / len(bpm_values)

        # 평균에서 ±8을 벗어난 곡 제거
        selected_songs = [song for song in selected_songs if abs(song[1] - bpm_avg) <= 8]

        # 부족한 곡을 채우기 위해 사용할 후보 필터링 (BPM 범위 내에서만 선택 가능)
        remaining_songs = [song for song in all_songs if song not in selected_songs and abs(song[1] - bpm_avg) <= 8]

        # 부족한 곡 채우기
        needed = num - len(selected_songs)
        if needed > 0:
            if len(remaining_songs) < needed:
                raise ValueError(f"BPM 조건을 만족하는 {num}곡을 찾을 수 없습니다.")
            selected_songs.extend(random.sample(remaining_songs, needed))

        # 최종적으로 30곡이 완성되었으면 반환
        if len(selected_songs) == num:
            return selected_songs


# sound_path = "/Users/honglab/Desktop/lofi-takoyaki/epidemicsound/lofi-hiphop-laidback"

# mood_list = ["Dreamy", "Relaxing", "Sentimental", "Peaceful"]

# try:
#     selected_songs = filter_and_select_songs(os.listdir(sound_path), mood_list)
#     for song in selected_songs:
#         print(song)
# except ValueError as e:
#     print(e)
