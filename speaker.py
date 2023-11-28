import pandas as pd
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

excel_file_path = 'suncheon_bus.xlsx'
df = pd.read_excel(excel_file_path)

def find_bus_numbers(source, destination):
    matching_routes = df[df['노선순서'].apply(lambda x: source in x and destination in x)]
    
    if not matching_routes.empty:
        # 출발지와 목적지의 인덱스를 가져옴
        source_index = matching_routes['노선순서'].apply(lambda x: x.index(source) if source in x else -1)
        dest_index = matching_routes['노선순서'].apply(lambda x: x.index(destination) if destination in x else -1)
        
        # 출발지와 목적지가 순서에 맞게 있는 경우에만 해당 버스를 반환
        valid_routes = matching_routes[(source_index >= 0) & (dest_index >= 0) & (source_index < dest_index)]
        
        if not valid_routes.empty:
            bus_numbers = valid_routes['버스번호'].tolist()
            return bus_numbers
    return None

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

def speak(text):
    print(f'[인공지능] {text}')
    tts = gTTS(text=text, lang='ko')
    tts.save('output.mp3')
    playsound('output.mp3')

def preprocess_location(location):
    # 띄어쓰기 없이 인식하기 위해 띄어쓰기를 모두 제거
    return location.replace(" ", "")

recognizer = sr.Recognizer() # 마이크 입력 후 인식
microphone = sr.Microphone() # 마이크 입력

while True:
    user_input = listen(recognizer, microphone)
    
    if user_input:
        if "에서" in user_input and "으로" in user_input: # 음성이 '~에서 ~으로'라고 입력 되면
            source = user_input.split("에서")[0].strip() # 출발지
            destination = user_input.split("에서")[1].split("으로")[0].strip() # 목적지
            
            # 띄어쓰기 없이 인식하도록 수정
            source = preprocess_location(source) # 음성인식으로 입력된 단어에서 공백을 없앰 - 출발지
            destination = preprocess_location(destination) # 음성인식으로 입력된 단어에서 공백을 없앰 - 목적지
            
            print(f"출발지: {source}, 목적지: {destination}")
            bus_numbers = find_bus_numbers(source, destination) # 출발지와 목적지에 맞는 버스 노선을 검색 후 버스 번호를 저장
            
            if bus_numbers:
                bus_numbers_str = ", ".join(map(lambda x: f"{x}번", bus_numbers)) # 버스 번호가 여러 개일시 , 를 이용하여 str에 저장
                speak(f"{source}에서 {destination}까지 운행하는 버스는 {bus_numbers_str} 버스입니다.")
            else:
                speak(f"{source}에서 {destination}까지 운행하는 버스가 없습니다.")
        elif "에서" in user_input and "로" in user_input: # 음성이 '~에서 ~로'라고 입력 되면
            source = user_input.split("에서")[0].strip() # 출발지
            destination = user_input.split("에서")[1].split("으로")[0].strip() # 목적지
            
            # 띄어쓰기 없이 인식하도록 수정
            source = preprocess_location(source) # 음성인식으로 입력된 단어에서 공백을 없앰 - 출발지
            destination = preprocess_location(destination) # 음성인식으로 입력된 단어에서 공백을 없앰 - 목적지
            
            print(f"출발지: {source}, 목적지: {destination}")
            bus_numbers = find_bus_numbers(source, destination) # 출발지와 목적지에 맞는 버스 노선을 검색 후 버스 번호를 저장
            
            if bus_numbers:
                bus_numbers_str = ", ".join(map(lambda x: f"{x}번", bus_numbers)) # 버스 번호가 여러 개일시 , 를 이용하여 str에 저장
                speak(f"{source}에서 {destination}까지 운행하는 버스는 {bus_numbers_str} 버스입니다.")
            else:
                speak(f"{source}에서 {destination}까지 운행하는 버스가 없습니다.")
        else:
            speak("출발지와 목적지를 다시 말해주세요.")
    else:
        speak("음성으로 입력하세요.")
