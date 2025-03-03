import time, json, shutil, os
import unicodedata

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.options import Options

URL='https://www.epidemicsound.com/music/genres/lo-fi-hip-hop/?moods=laid-back&vocals=false'

profile_path = '/Users/honglab/Desktop/lofi-takoyaki/lofi-takoyaki/selenium_userdata/tmp'
download_path = '/Users/honglab/Desktop/lofi-takoyaki/epidemicsound/lofi-hiphop-laidback/'

options = Options()
options.add_argument(f'user-data-dir={profile_path}')
options.add_argument('disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=options)
driver.get(URL)

print('current_url : ' + driver.current_url)
print('title : ' + driver.title)
time.sleep(5)

def normalize_to_ascii(text):
    # 유니코드 정규화를 통해 영어와 가까운 문자로 변환
    normalized_text = unicodedata.normalize('NFKD', text)
    
    # 영어 알파벳이 아닌 문자는 제거하고 ASCII 문자만 남김
    ascii_text = ''.join(c for c in normalized_text if c.isascii())
    
    return ascii_text

def get_element(params: list):
    try: return WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(tuple(params))
    )
    except: return None

def get_and_click_try(name: str, params: list, element=None):
    if element is None:
        button = get_element(params)
    else:
        button = element.find_element(*params)
    
    if button is not None:
        # print(button)
        # print(dir(button))
        # 버튼 클릭
        try:
            button.click()
            print(f"✅ '{name}' 버튼을 성공적으로 클릭했습니다.")
            return True
        except Exception as e:
            print(f"❌ '{name}' 버튼을 찾았으나 클릭할 수 없습니다: {e}")
            return False

    else:
        print(f"❌ '{name}' 버튼을 찾을 수 없거나 클릭할 수 없습니다.")
        return False

def get_data_index(track):
    try:
        parent_div = track.find_element(By.XPATH, "./ancestor::div[@data-index]")
        data_index = parent_div.get_attribute("data-index")
        return int(data_index)
    except Exception as e:
        print(f'get_data_index 도중 에러 발생: {e}')
        return None

def file_mv(title, runningtime, bpm, additional_mood):
    source_dir = os.path.expanduser("~/Downloads/")
    dest_dir = os.path.expanduser(download_path)

    # 대상 폴더가 없으면 생성
    os.makedirs(dest_dir, exist_ok=True)
    
    file_prefix = f'ES_{title}'
    new_filename = normalize_to_ascii(f'{additional_mood}_{bpm}_{runningtime.replace(':', '-')}__{title}.mp3')
    dest_path = os.path.join(dest_dir, new_filename)

    # 다운로드 폴더에서 파일 찾기 및 이동
    for filename in os.listdir(source_dir):
        if filename.startswith(file_prefix):  # 특정 문자열로 시작하는 파일 찾기
            source_path = os.path.join(source_dir, filename)

            # 이미 파일이 존재하는 경우 pass
            if os.path.exists(dest_path):
                print(f"⚠️ {dest_path} 이미 존재하여 이동하지 않음.")
                os.remove(source_path)
                print(f"삭제 완료: {filename}")
                return

            # 파일 이동
            shutil.move(source_path, dest_path)
            print(f"Moved: {filename} → {dest_path}")
            break

def main():
    current_index = 0
    # View more 전부 누르고 시작
    while get_and_click_try("View more", [By.XPATH, "//button[contains(text(), 'View more')]"]):
        time.sleep(2)
    
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

    while True:
        print(f'current index : {current_index}')
        track_div_xpath = f"//div[@data-index='{current_index}']//div[@data-testid='track-row']"
        try:
            track_div = driver.find_element(By.XPATH, track_div_xpath)
        except Exception as e:
            print("❌ 더 이상 트랙이 없습니다. :", e)
            break

        try:
            # track_div = driver.find_element(By.XPATH, track_div_xpath)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", track_div)
            track_str_list = track_div.text.split('\n')
            # 'Shadi\nHATAMITSUNAMI\n3:02\n96 BPM\nAfrobeatsLo-Fi Hip Hop\nHopefulLaid Back'

            title = track_str_list[0]
            print('title : ' + title)
            runningtime = track_str_list[2]
            print('runningtime : ' + runningtime)
            bpm = track_str_list[3].replace(' BPM', '')
            print('bpm : ' + bpm)
            additional_mood = track_str_list[-1].replace('Laid Back', '')
            print('additional_mood : ' + additional_mood)

            if os.path.exists(os.path.join(download_path, normalize_to_ascii(f'{additional_mood}_{bpm}_{runningtime.replace(':', '-')}__{title}.mp3'))):
                print('이미 다운받은 곡이므로 건너뜁니다...')
                current_index += 1
                continue

            else:
                print(track_div.text)
                print(title)
                time.sleep(10)
            
            get_and_click_try(f'{title} Download1', [By.XPATH, ".//button[starts-with(@aria-label, 'Download')]"], track_div)
            time.sleep(2)
            get_and_click_try(f'{title} Download2', [By.XPATH, "//button[contains(text(), 'Download') and @aria-disabled='false']"], track_div)
            time.sleep(3)

            file_mv(title, runningtime, bpm, additional_mood)
        
        except Exception as e:
            print("❌ 문제가 발생했습니다:", e)
            print("다음 번호로 넘어갑니다.")
        
        current_index += 1

main()
time.sleep(1000)
