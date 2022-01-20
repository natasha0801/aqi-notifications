from bs4 import BeautifulSoup
from twilio.rest import Client
from pygame import mixer
import requests, winsound, datetime, time
import numpy as np
import matplotlib.pyplot as plt
account_sid = 'placeholder' # replace with user's account sid
auth_token = 'placeholder' # replace with user's account sid
phone_number = 'whatsapp:+11234567890' # replace with user phone
client = Client(account_sid, auth_token)
state = input('State: ')
city = input('City: ')
period = input('Monitoring Period (Minutes): ')
dataTimes = []
dataAqis = []
window = 24
badAir = False
threshold = 150
try:
    period = float(period.strip()) / 60.0
except:
    period = 0.25
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
        aqi = (p[0].get_text()).strip()
        print('Current AQI: ' + aqi)
        try:
            aqi = int(aqi)
            if (len(dataTimes) < 1):
                starttime = time.time()
                fig, ax = plt.subplots()
                ax.set_xlim([0, window])
                ax.set_ylim([0, 500])
                dataTimes.extend([0])
                dataAqis.extend([aqi])
                line, = ax.plot(dataTimes, dataAqis, '-o')
                plt.title('AQI vs. Time')
                plt.xlabel('Time Since Start (Hours)')
                plt.ylabel('AQI')
                plt.grid()
                fig.show()
                fig.canvas.flush_events()
            else:
                currentHrs = (time.time() - starttime) / 60 / 60
                dataTimes.extend([currentHrs])
                dataAqis.extend([aqi])
                if currentHrs > window - period:
                    ax.set_xlim([currentMinutes - window + period, currentMinutes + period])
                line.set_data(dataTimes, dataAqis)
                fig.canvas.draw()
                fig.canvas.flush_events()
            plt.pause(5)
            if aqi < threshold and badAir == True:
                print('AQI is under ' + str(threshold) + '.')
                string = 'Air Monitor: AQI is now in acceptable range (currently at ' + str(aqi) + ').'
                badAir = False
                try:
                    message = client.messages.create( 
                                  from_='whatsapp:+14155238886',  
                                  body=string,      
                                  to=phone_number
                            )
                except:
                    print('ERROR: Failed to send WhatsApp message.')
            elif aqi >= threshold and badAir == False:
                print('AQI is over ' + str(threshold) + '.')
                string = 'Air Monitor: AQI is now in unhealthy range (currently at ' + str(aqi) + ').'
                badAir = True
                try:
                    message = client.messages.create( 
                                  from_='whatsapp:+14155238886',  
                                  body=string,      
                                  to=phone_number
                            )
                    print('Notification sent.')
                except:
                    print('ERROR: Failed to send WhatsApp message.')
        except:
            print('ERROR: AQI cannot be converted to numerical value.')
    except:
        print('ERROR: failed to access IQAir.com.')
    time.sleep(60 * 60 * period)
