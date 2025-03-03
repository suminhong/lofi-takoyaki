import os, json, urllib.request
from openai import OpenAI
openai_client = OpenAI()

# 현재 파일(utils/openai.py)의 디렉토리 경로를 기준으로 상대 경로 계산
current_dir = os.path.dirname(os.path.abspath(__file__))
prompt_dir = os.path.join(os.path.dirname(current_dir), 'prompt')

def create_chat(prompt) -> str:
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "developer",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content

def create_image(prompt, size="1792x1024") -> str:
    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
    )

    return response.data[0].url

def create_subject_file(genre, lang, subject_file) -> dict:
    prompt_file = os.path.join(prompt_dir, f"{genre}-{lang}.txt")
    
    with open(prompt_file, "r") as f:
        prompt = f.read()
    
    json_output = create_chat(prompt).split('```json')[1].split('```')[0]
    print(json_output)
    
    with open(subject_file, "w") as f:
        f.write(json_output)
    
    return json.loads(json_output)

def create_image_file(title, image_webp_file):
    image_url = create_image(f"{title} 이란 영상 제목에 맞는 16:9 비율의 이미지를 생성해 주세요.")
    print(image_url)

    # urlretrieve: URL을 통해 생성된 이미지를 로컬에 저장
    urllib.request.urlretrieve(image_url, image_webp_file)