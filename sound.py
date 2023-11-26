import pandas as pd

# 엑셀 파일에서 데이터 읽어오기
df = pd.read_excel('suncheon_bus.xlsx')

# 데이터를 딕셔너리로 변환
bus_stops = df.set_index('노선')['정류장'].apply(lambda x: x.split(',')).to_dict()

# 음성 인식된 명령어를 처리하는 함수
def process_command(command):
    # command를 파싱하여 출발지와 목적지 추출
    parts = command.split('에서')
    if len(parts) != 2:
        return "명령어를 이해하지 못했습니다."

    start_point, end_point = parts[0].strip(), parts[1].strip()

    # 노선이 존재하는지 확인
    for route, stops in bus_stops.items():
        if start_point in stops and end_point in stops:
            return f"{route}이 운행합니다."
    
    return "해당하는 운행하는 버스가 없습니다."

# 테스트
user_command = "순천역에서 경찰서로 갈거야"
response = process_command(user_command)
print(response)

user_command = "팔마경기장에서 옥천 현대로 갈거야"
response = process_command(user_command)
print(response)