import urequests
import network
import time
import os

SERVER_URL = 'http://192.168.45.90:3000/upload'

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
def delete_file(file_name):
    os.remove(file_name)
    print("m7ito")

# def send_data(ir_reading, red_reading, cpt, current_time):
#     print ("Sending data to server (" + str(cpt) + ")........")
#     data = {'ir_value': ir_reading, 'red_value': red_reading, 'cpt': cpt, 'time': current_time}
#     response = urequests.post(SERVER_URL, json=data)
#     print(response.text)

def send_data(file_name: str):
    # Open the CSV file you want to send
    try:
        file_contents = open(file_name, 'rb').read()
    except OSError:
        print(f"File not found: {file_name}")
        exit(1)

    # Prepare the headers and data for the POST request
    headers = {'Content-Type': 'application/octet-stream'}
    # headers = {
    #     'Content-Type': 'text/csv',  # Set the appropriate content type for CSV
    #     'Content-Disposition': 'attachment; filename=sensor_data.csv'  # Specify the filename
    # }

    # Send the file to the server in the request body
    data = {"file_body" : file_contents, "file_name": file_name, "headers": headers}
    try:
        response = urequests.post(SERVER_URL, json=data)
        if response.status_code == 200:
            print("Data sent to server successfully")
            delete_file(file_name)
        else:
            print("Failed to send data to server. Status code:", response.status_code)
        response.close()
    except Exception as e:
        print("Error sending data to server:", e)
        
        