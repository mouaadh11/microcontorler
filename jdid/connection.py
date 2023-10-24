import urequests
import network
import time
import ujson

SERVER_URL = 'http://192.168.1.39:3000/data'

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

# def send_data(ir_reading, red_reading, cpt, current_time):
#     print ("Sending data to server (" + str(cpt) + ")........")
#     data = {'ir_value': ir_reading, 'red_value': red_reading, 'cpt': cpt, 'time': current_time}
#     response = urequests.post(SERVER_URL, json=data)
#     print(response.text)

def send_data_to_server(file_name: str):
    url = SERVER_URL

    # Open the CSV file you want to send
    with open("example.csv", "r") as file:
        file_content = file.read()
    
    headers = {
        'Content-Type': 'text/csv',  # Set the appropriate content type for CSV
        'Content-Disposition': 'attachment; filename=example.csv'  # Specify the filename
    }
    
    try:
        response = urequests.post(url, data=file_content, headers=headers)
        if response.status_code == 200:
            print("Data sent to server successfully")
        else:
            print("Failed to send data to server. Status code:", response.status_code)
        response.close()
    except Exception as e:
        print("Error sending data to server:", e)