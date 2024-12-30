from django.shortcuts import render
from .models import *
import requests
import math
import os
import cv2
import threading
import playsound
import smtplib
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse
from datetime import datetime
import os
from django.conf import settings
from django.core.files.storage import default_storage

fire_cascade_path = os.path.join(os.path.dirname(__file__), 'fire_detection_cascade_model.xml')
fire_cascade = cv2.CascadeClassifier(fire_cascade_path)
is_recording = False
recording_lock = threading.Lock()
alarm_lock = threading.Lock()
mail_lock = threading.Lock()
recipient_mail = "b3nnie@proton.me"
recipient_mail = recipient_mail.lower()
runOnce = False
video_out = None  # Declare video_out as a global variable

def play_alarm_sound_function():
    with alarm_lock:
        alarm_sound_path = os.path.join(os.path.dirname(__file__), 'Alarm Sound.mp3')
        playsound.playsound(alarm_sound_path, True)  # Adjust path
        print("Fire alarm end")

def send_mail_function():
    with mail_lock:
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login("benmalunga041@gmail.com", 'palib')
            server.sendmail('b3nnie@proton.me', recipient_mail, "Warning fire accident has been reported")
            print("Alert mail sent successfully to {}".format(recipient_mail))
            server.close()
        except Exception as e:
            print(e)

def start_video_recording():
    global is_recording, video_out
    with recording_lock:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        video_out = cv2.VideoWriter(f'recordings/fire_detection_{current_time}.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
        is_recording = True

def release_video_writer():
    global video_out
    with recording_lock:
        if video_out is not None and video_out.isOpened():
            video_out.release()

def stop_video_recording():
    global is_recording
    with recording_lock:
        is_recording = False
        release_video_writer()


def get_frame():
    global is_recording, runOnce, video_out

    
    vid = cv2.VideoCapture(0)

    while True:
        alarm_status = False
        ret, frame = vid.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

        for (x, y, w, h) in fire:
            cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 2)

            if not is_recording:
                threading.Thread(target=start_video_recording).start()

            print("Fire alarm initiated")
            threading.Thread(target=play_alarm_sound_function).start()

            if not runOnce:
                print("Mail send initiated")
                threading.Thread(target=send_mail_function).start()
                runOnce = True

        if is_recording:
            if video_out is not None:
                video_out.write(frame)

        _, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()
    stop_video_recording()

def video_feed(request):
    return StreamingHttpResponse(get_frame(), content_type='multipart/x-mixed-replace; boundary=frame')


def get_user_location(request):
    try:
        # Use ipinfo.io to get the user's IP address and location information
        ipinfo_response = requests.get('https://ipinfo.io')
        ipinfo_data = ipinfo_response.json()

        # Extract latitude and longitude from the response
        local_latitude, local_longitude = map(float, ipinfo_data['loc'].split(','))

        return local_latitude, local_longitude

    except Exception as e:
        # Handle exceptions (e.g., if the API request fails)
        print(f"Error getting user location: {str(e)}")
        return None, None

def webcam(request):
    # Get user's location
    local_latitude, local_longitude = get_user_location(request)

    if local_latitude is None or local_longitude is None:
        # Handle the case where location couldn't be determined
        context = {
            "error_message": "Unable to determine user location.",
        }
        return render(request, 'webcam.html', context)

    # Get weather information for the specified coordinates
    api_key = 'e7da9729ea940df88e6fc98e7d07dc82'
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={local_latitude}&lon={local_longitude}&appid={api_key}"

    try:
        w_dataset = requests.get(url).json()

        # Check if 'city' key exists in the response
        if 'city' in w_dataset:
            weather_info = {
                "city_name": w_dataset["city"].get("name", "N/A"),
                "city_country": w_dataset["city"].get("country", "N/A"),
                "wind": w_dataset.get('list', [])[0].get('wind', {}).get('speed', "N/A"),
                "degree": w_dataset['list'][0]['wind']['deg'],
                "status": w_dataset['list'][0]['weather'][0]['description'],
                "cloud": w_dataset['list'][0]['clouds']['all'],
                'date': w_dataset['list'][0]["dt_txt"],
                'date1': w_dataset['list'][1]["dt_txt"],
                'date2': w_dataset['list'][2]["dt_txt"],
                'date3': w_dataset['list'][3]["dt_txt"],
                'date4': w_dataset['list'][4]["dt_txt"],
                'date5': w_dataset['list'][5]["dt_txt"],
                'date6': w_dataset['list'][6]["dt_txt"],

                "temp": round(w_dataset["list"][0]["main"]["temp"] - 273.0),
                "temp_min1": math.floor(w_dataset["list"][1]["main"]["temp_min"] - 273.0),
                "temp_max1": math.ceil(w_dataset["list"][1]["main"]["temp_max"] - 273.0),
                "temp_min2": math.floor(w_dataset["list"][2]["main"]["temp_min"] - 273.0),
                "temp_max2": math.ceil(w_dataset["list"][2]["main"]["temp_max"] - 273.0),
                "temp_min3": math.floor(w_dataset["list"][3]["main"]["temp_min"] - 273.0),
                "temp_max3": math.ceil(w_dataset["list"][3]["main"]["temp_max"] - 273.0),
                "temp_min4": math.floor(w_dataset["list"][4]["main"]["temp_min"] - 273.0),
                "temp_max4": math.ceil(w_dataset["list"][4]["main"]["temp_max"] - 273.0),
                "temp_min5": math.floor(w_dataset["list"][5]["main"]["temp_min"] - 273.0),
                "temp_max5": math.ceil(w_dataset["list"][5]["main"]["temp_max"] - 273.0),
                "temp_min6": math.floor(w_dataset["list"][6]["main"]["temp_min"] - 273.0),
                "temp_max6": math.ceil(w_dataset["list"][6]["main"]["temp_max"] - 273.0),

                "pressure": w_dataset["list"][0]["main"]["pressure"],
                "humidity": w_dataset["list"][0]["main"]["humidity"],
                "sea_level": w_dataset["list"][0]["main"]["sea_level"],

                "weather": w_dataset["list"][1]["weather"][0]["main"],
                "description": w_dataset["list"][1]["weather"][0]["description"],
                "icon": w_dataset["list"][0]["weather"][0]["icon"],
                "icon1": w_dataset["list"][1]["weather"][0]["icon"],
                "icon2": w_dataset["list"][2]["weather"][0]["icon"],
                "icon3": w_dataset["list"][3]["weather"][0]["icon"],
                "icon4": w_dataset["list"][4]["weather"][0]["icon"],
                "icon5": w_dataset["list"][5]["weather"][0]["icon"],
                "icon6": w_dataset["list"][6]["weather"][0]["icon"],
                # Add other weather information as needed
            }
            context = {
                "weather_info": weather_info,
            }
        else:
            context = {
                "error_message": "City information not found in the API response.",
            }

    except Exception as e:
        context = {
            "error_message": f"Error fetching weather data: {str(e)}"
        }

    return render(request, 'webcam.html', context)
