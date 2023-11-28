import pandas as pd
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# 엑셀 파일에서 데이터를 읽어옴
excel_file_path = 'suncheon_bus.xlsx'
df = pd.read_excel(excel_file_path)

# 출발지와 목적지에 해당하는 버스 번호를 찾는 함수
def find_bus_numbers(source, destination):
    matching_routes = df[df['노선순서'].apply(lambda x: source in x and destination in x)]
    
    if not matching_routes.empty:
        bus_numbers = matching_routes['버스번호'].tolist()
        return bus_numbers
    else:
        return None

# 사용자 음성을 입력받는 함수
def listen(recognizer, microphone):
    with microphone as source:
        try:
            speak("어디에서 어디로 가시려나요?")
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='ko')
            print(f'[나] {text}')
            return text
        except sr.UnknownValueError:
            print('음성 인식 실패. 다시 시도해주세요.')
            return None
        except sr.RequestError as e:
            print(f'음성 인식 요청 실패: {e}')
            return None

# 음성으로 메시지를 출력하는 함수
def speak(text):
    print(f'[인공지능] {text}')
    tts = gTTS(text=text, lang='ko')
    tts.save('output.mp3')
    playsound('output.mp3')

# 띄어쓰기 없이 인식하기 위해 띄어쓰기를 모두 제거하는 함수
def preprocess_location(location):
    return location.replace(" ", "")

# 음성 인식 및 처리 루프
recognizer = sr.Recognizer()
microphone = sr.Microphone()

while True:
    user_input = listen(recognizer, microphone)
    
    if user_input:
        # "~에서 ~으로" 또는 "~에서 ~로" 패턴에 따라 출발지와 목적지를 구분
        if "에서" in user_input and ("으로" in user_input or "로" in user_input):
            source = user_input.split("에서")[0].strip()
            destination = user_input.split("에서")[1].split("으로")[0].split("로")[0].strip()
            
            # 띄어쓰기 없이 인식하도록 수정
            source = preprocess_location(source)
            destination = preprocess_location(destination)
            
            print(f"출발지: {source}, 목적지: {destination}")
            bus_numbers = find_bus_numbers(source, destination)
            
            if bus_numbers:
                bus_numbers_str = ", ".join(map(lambda x: f"{x}번", bus_numbers))
                speak(f"{source}에서 {destination}까지 운행하는 버스는 {bus_numbers_str} 버스입니다.")
            else:
                speak(f"{source}에서 {destination}까지 운행하는 버스가 없습니다.")
        else:
            speak("출발지와 목적지를 다시 말해주세요.")
    else:
        speak("음성으로 입력하세요.")
