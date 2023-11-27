import pandas as pd
import speech_recognition as sr
import networkx as nx
from gtts import gTTS
from playsound import playsound

# Load Excel data
excel_file_path = 'bus_routes.xlsx'  # 파일 경로를 실제 파일의 경로로 변경하세요.
df = pd.read_excel(excel_file_path)

# Create a graph from the bus routes data
G = nx.Graph()
for _, row in df.iterrows():
    route_stops = [stop.strip() for stop in row['노선 순서'].split(',')]
    for i in range(len(route_stops) - 1):
        G.add_edge(route_stops[i], route_stops[i+1], bus_number=row['버스번호'])

def find_bus_numbers(source, destination):
    try:
        paths = list(nx.all_shortest_paths(G, source=source, target=destination))
        bus_numbers = set(G[path[0]][path[1]]['bus_number'] for path in paths)
        
        if bus_numbers:
            return f"출발지 {source}에서 목적지 {destination}까지 운행하는 버스 번호는 {', '.join(map(str, bus_numbers))}입니다."
        else:
            return "해당하는 운행하는 버스가 없습니다."
    except nx.NetworkXNoPath:
        return "해당하는 운행하는 버스가 없습니다."

def listen(recognizer, microphone):
    with microphone as source:
        try:
            print("무엇을 도와드릴까요?")
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='ko')
            print(f'[나] {text}')
            return text
        except sr.UnknownValueError:
            print('음성 인식 실패. 텍스트로 입력하세요.')
            return None
        except sr.RequestError as e:
            print(f'음성 인식 요청 실패: {e}')
            return None

def speak(text):
    print(f'[인공지능] {text}')
    tts = gTTS(text=text, lang='ko')
    tts.save('output.mp3')
    playsound('output.mp3')

recognizer = sr.Recognizer()
microphone = sr.Microphone()

while True:
    user_input = listen(recognizer, microphone)
    
    if user_input:
        if "에서" in user_input and "으로 갈 거야" in user_input:
            source = user_input.split("에서")[0].strip()
            destination = user_input.split("에서")[1].split("으로 갈 거야")[0].strip()
            print(f"출발지: {source}, 목적지: {destination}")
            bus_info = find_bus_numbers(source, destination)
            speak(bus_info)
        elif "에서" in user_input and "로 갈 거야" in user_input:
            source = user_input.split("에서")[0].strip()
            destination = user_input.split("에서")[1].split("로 갈 거야")[0].strip()
            print(f"출발지: {source}, 목적지: {destination}")
            bus_info = find_bus_numbers(source, destination)
            speak(bus_info)
        else:
            print("지원하지 않는 명령 또는 입력입니다.")
    else:
        print("텍스트로 입력하세요.")
