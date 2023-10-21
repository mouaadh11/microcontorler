import urequests
import network
import time

SERVER_URL = 'http://192.168.1.41:3000/data'

def do_connect(ssid: str, password: str):
    wlan = network.WLAN(network.STA_IF)
    #restarting wifi to avoid any errors
    wlan.active(False)
    time.sleep(0.5)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('\nnetwork config:', wlan.ifconfig())

def send_data(ir_reading, red_reading, cpt, current_time):
    print ("Sending data to server (" + str(cpt) + ")........")
    data = {'ir_value': ir_reading, 'red_value': red_reading, 'cpt': cpt, 'time': current_time}
    response = urequests.post(SERVER_URL, json=data)
    print(response.text)