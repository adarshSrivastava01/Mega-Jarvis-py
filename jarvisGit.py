import pyttsx3
import sys
import time
import datetime
import speech_recognition as sr
import wikipedia
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests, json

w_api_key = 'Paste weather API Key here.'     # Paste weather API Key here.
w_base_url = 'Paste weather URL here.'  # Paste weather URL here.
n_base_url = 'Paste News URL here.' # Paste News URL here.
n_api_key = 'Paste news API Key here.' # Paste news API Key here.
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')   
engine.setProperty('voice', voices[0].id)  # Replace '0' by '1' for Girl Assistant.

def speak(audio):
    """
    Function which takes string as Input.
    speaks the string with Microsft Speech API SAPI5
    """
    engine.say(audio)
    engine.runAndWait()

def listener():
    """
    Function which listens from the source
    returns String as query
    """
    recognisedAudio = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        recognisedAudio.pause_threshold = 1
        audio = recognisedAudio.listen(source)
    try:
        print('Recoginizing....')
        query = recognisedAudio.recognize_google(audio, language='en-in')
        print(f'User said: {query}\n')
        speak(query)
    except Exception:
        print('Say that Again..')
        return 'None'
    return query

def wish():
    """
    Function which wishes the user according to time in 24-Hour Format
    """
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak('Good Morning!')
    elif hour>=12 and hour<18:
        speak('Good Afternoon!')
    else:
        speak('Good Evening!')
    speak('Hey! I am Jarvis, how can I help You.')

if __name__ == "__main__":
    wish()

    while True:
        query = listener().lower()

        if 'wikipedia' in query:
            """
            It searches for the string 'wikipedia' in query if exists then
            replaces 'wikipedia' by ''
            and searches for the remaining query in wikipedia and speaks sentences
            """
            speak('Please wait...')
            query = query.replace('wikipedia', ' ')
            results = wikipedia.summary(query, sentences=2)
            speak('This is what I got in Wikipedia: ')
            speak(results)
            speak('If You want to continue press Y: ')
            userChoice = input('If You want to continue press Y: ')
            if userChoice == 'y' or userChoice == 'Y':
                speak('Enter the No. of sentences you want from Wikipedia: ')
                sentenceNo = int(input('Enter the No. of sentences you want from Wikipedia: '))
                results = wikipedia.summary(query, sentences=sentenceNo)
                speak(results)
                print(results)
            else:
                print(results)

        elif 'youtube' in query:
            """
            It searches for the string 'youtube' in query if exists then
            It automatically opens Youtube for You in Chrome
            and asks for the thing which you want to play in youtube.
            and then plays that song.
            """
            speak('Which song you want to watch in youtube')
            userSong = listener().lower()
            browser = webdriver.Chrome('C:\webdrivers\chromedriver')
            browser.get("https://www.youtube.com")
            time.sleep(2)
            inputField = browser.find_elements_by_id('search')[0]
            inputField.send_keys(userSong)
            inputField.send_keys(Keys.ENTER)
            play = browser.find_element_by_xpath('//*[@id="video-title"]')
            play.click()
        
        elif 'weather' in query:
            """
            It searches for the string 'weather' in query if exists then
            asks for the city
            and tells about the Temprature, Humidity and Waether description.
            """
            speak('Please wait...')
            userCity = listener().lower()
            w_complete_url = w_base_url + 'q=' + userCity + '&appid=' + w_api_key  # Make Changes here according to your URL
            w_response = requests.get(w_complete_url)
            json_response = w_response.json()
            if json_response["cod"] != "404":
                y = json_response["main"]
                crnt_temp = y["temp"]
                crnt_humid = y["humidity"]
                z = json_response["weather"]
                wthr_des = z[0]["description"]
                speak('Temprature is ' + str(crnt_temp) + 'Humidity is ' + str(crnt_humid) + 'Weather description is ' + str(wthr_des))
                print('Temprature is ' + str(crnt_temp) + 'Humidity is ' + str(crnt_humid) + 'Weather description is ' + str(wthr_des))
            else:
                print('City Not Found.')
                speak('City Not Found.')

        elif 'news' in query:
            """
            It searches for the string 'news' in query if exists then
            and tells about the Top 10 News of that time.
            """
            speak('Please wait...')
            n_complete_url = n_base_url + '&apiKey=' + n_api_key  # Make Changes here according to your URL
            n_respond = requests.get(n_complete_url).json()
            article = n_respond['articles']
            result = []
            for each in article:
                result.append(each['title'])
            for i in range(len(result)):
                speak(result[i])
        
        elif 'time' in query:
            """
            It searches for the string 'time' in query if exists then
            tells the time.
            """
            Time = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f'The Time is {Time}')
            print(f'The Time is {Time}')

        elif 'exit' in query:
            speak('ThankYou.')
            sys.exit()