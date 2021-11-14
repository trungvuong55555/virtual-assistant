import speech_recognition as sr
import time
import wikipedia
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
import pyttsx3
from model import model_educational_admissions_consultant

model = model_educational_admissions_consultant()
wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()


def speak(text):
    print("Bot: {}".format(text))
    engine = pyttsx3.init()
    vi_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_viVN_An"
    engine.setProperty("voice", vi_voice_id)
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Bot đang nghe....")
        print("Tôi: ", end='')
        audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text
        except:
            print("...")
            return 0

def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            speak("Bot không nghe rõ. Bạn nói lại được không!")
    time.sleep(2)
    stop()
    return 0

def educational_admissions_consultant():
    speak("bạn muốn tư vấn gì nào?")
    text = get_text()
    result = model.predict(text)
    if result == "noanswer":
        speak("Thông tin này tôi không biết, bạn có thể liên hệ theo số điện thoại 12345 để được khoa tư vấn thêm")
        speak("Hoặc bạn có muốn tìm kiếm thông tin trên google không?")
        text1 = get_text()
        if "có" in text1 or "ok" in text1:
            open_google_and_search(text)
            return
        else:
            return

    speak(result)

def stop():
    speak("Tạm biệt!")

def hello():
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng bạn. Chúc bạn một ngày tốt lành.")
    elif 12 <= day_time < 18:
        speak("Chào buổi chiều bạn. Bạn đã dự định gì cho chiều nay chưa.")
    else:
        speak("Chào buổi tối bạn. Bạn đã ăn tối chưa nhỉ.")

def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak('Bây giờ là %d giờ %d phút' % (now.hour, now.minute))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d" %
              (now.day, now.month, now.year))
    else:
        speak("Bot chưa hiểu ý của bạn. Bạn nói lại được không?")


def open_google_and_search(text):
    speak('Okay!')
    driver = webdriver.Chrome(path)
    driver.get("https://www.google.com")
    que = driver.find_element_by_xpath("//input[@name='q']")
    que.send_keys(str(text))
    que.send_keys(Keys.RETURN)
    time.sleep(15)
    while True:
        speak("Bạn có muốn tiếp tục lướt web không?")
        text= get_text()
        if "có" in text or "ok" in text:
            time.sleep(20)
        else:
            driver.close()
            break


def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ?")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
                                                                           hourset = sunset.hour, minset = sunset.minute,
                                                                           temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
        speak(content)
        time.sleep(5)
    else:
        speak("Không tìm thấy địa chỉ của bạn")

def tell_me_about():
    try:
        speak("Bạn muốn nghe về gì ạ")
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        time.sleep(10)
        for content in contents[1:]:
            speak("Bạn muốn nghe thêm không?")
            ans = get_text()
            if "có" not in ans:
                break
            speak(content)
            time.sleep(3)

        speak('Cảm ơn bạn đã lắng nghe!!!')
    except:
        speak("Bot không hiểu bạn nói. Xin mời bạn nói lại")


def introduce():
    speak("""Tôi có thể thực hiện các thao tác sau đây:
        1. Chào hỏi
        2. Hiển thị giờ
        3. Tìm kiếm trên Google 
        4. Tư vấn tuyển sinh cho khoa thì hãy nói tư vấn
        5. Dự báo thời tiết
        6. Tra cứu với wikipedia hãy nói từ điển
        """)

def assistant():
    speak("Xin chào, tôi là trợ lý ảo tư vấn tuyển sinh khoa công nghệ thông tin trường đại học Công Nghiệp Hà Nội?")
    introduce()
    while True:
        text = get_text()
        if not text:
            break
        elif "dừng" in text or "tạm biệt" in text or "chào robot" in text or "kết thúc" in text or "tắt" in text:
            stop()
            break
        elif "có thể làm gì" in text:
            introduce()
        elif "chào" in text:
            hello()
        elif "hiện tại" in text or "giờ" in text:
            get_time(text)
        elif "tìm" in text:
            open_google_and_search(text)
        elif "thời tiết" in text or "nhiệt độ" in text:
            current_weather()
        elif "từ điển" in text:
            tell_me_about()
        elif "tư vấn" in text:
            educational_admissions_consultant()
        else:
            speak("Bạn cần Bot giúp gì ạ?")

assistant()