import time
import os
import speech_recognition as st
from gtts import gTTS
from playsound import playsound
basic = "무엇을 도와드릴까요?"
# 음성인식 듣기(STT) : 내 음성을 텍스트로~
def listen(recognizer, microphone):
    with microphone as source:
        speak(basic)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='ko')
            print('[나]' + text)
            answer(text)
        except st.UnknownValueError:
            print('인식 실패')
        except st.RequestError as e:
            print('요청 실패: {0}'.format(e))

# 대답
def answer(input_text):
    answer_text = ''
    if '안녕' in input_text:
        answer_text = '안녕하세요? 반갑습니다.'
    elif '조원이름' in input_text:
        answer_text = '송창석,김경윤,김예진,이정호,이주현,장태영,황승훈. 이렇게 7명 있습니다.'
    elif '상황' in input_text:
        answer_text = '지금 동아리 상황은 조졌습니다.'
    elif '고마워' in input_text:
        answer_text = '별 말씀을요!'
    elif '종료' in input_text:
        answer_text = '다음에 또 만나요.'
        exit()
    else:
        answer_text = '뭔 소리야 다시 말해줘'
    speak(answer_text)

# 소리내어 읽기(TTS)
def speak(text):
    print('[인공지능]' + text)
    file_name = 'voice.mp3'
    tts = gTTS(text=text, lang='ko')
    tts.save(file_name)
    playsound(file_name)
    if os.path.exists(file_name):
        os.remove(file_name)

r = st.Recognizer()
m = st.Microphone()

while True:
    listen(r, m)
    time.sleep(0.1)