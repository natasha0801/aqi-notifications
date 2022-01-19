from bs4 import BeautifulSoup
from twilio.rest import Client
from pygame import mixer
import requests, winsound, datetime, time
account_sid = 'AC38f54cecc58e876c01216e5c454ff367'
auth_token = 'e039f4c11845e0d5d8162e4b1e13d2d9'
client = Client(account_sid, auth_token)
state = input('State: ')
city = input('City: ')
threshold = input('AQI Threshold: ')
period = input('Monitoring Period (Minutes): ')
try:
    threshold = int(threshold.strip())
except:
    threshold = 150
try:
    period = int(period.strip())
except:
    period = 15
state = state.strip().lower()
city = city.strip().lower()
url = 'https://www.iqair.com/us/usa/'+state+'/'+city
while True:
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        p = soup.find_all('p', class_='aqi-value__value')
        print('------------------------------------------')
        print(datetime.datetime.now())
        try:
            aqi = (p[0].get_text()).strip()
            print('Current AQI: ' + aqi)
            if int(aqi) < threshold:
                mixer.init()
                mixer.music.load('and-his-name-is-john-cena-1.mp3')
                mixer.music.play()
                print('AQI is under ' + str(threshold) + '.')
                string = 'AQI Alert: Current AQI is under ' + str(threshold) + ' (currently at ' + str(aqi) + ').'
                try:
                    message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body=string,      
                              to='whatsapp:+19168609619' 
                            )
                except:
                    print('Error: could not send WhatsApp notification')
            except:
                print('Error: could not retrieve AQI')
    except:
        print('Error: could not retrieve page from IQAir')
    time.sleep(60 * period)

    
