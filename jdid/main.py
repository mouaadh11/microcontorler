# main.py
import time
import sensor
import connection
from utime import sleep, ticks_diff, ticks_ms

def record_to_csv(filename, data):
    with open(filename, "a") as file:
        file.write(data + "\n")

# Create a CSV file
csv_filename = "sensor_data.csv"

def main():
    sensor1, default_value = sensor.setUp()
    cpt = 0
    while True:
        cpt += 1
        ir_reading, red_reading = sensor.get_data(sensor1, default_value)
        # current_time = str(time.localtime()[3] +1) + ":" + str(time.localtime()[4]) + ":" + str(time.localtime()[5])
        current_time = time.localtime()
        
        # Record data to CSV
        record_to_csv(csv_filename, f"{ir_reading},{red_reading},{current_time}")

        print("ir_reading = ", ir_reading)
        print("red_reading = ", red_reading)
        
        # Send data to the server every 60 seconds
        if current_time[5] % 60 == 0:
            connection.send_data(csv_filename)
        
        time.sleep(1)

        #try:
            #connection.send_data(ir_reading, red_reading, cpt, current_time)
        #except OSError:
            #print("Error while sending data to server")

        # time.sleep(0.5)

if __name__ == '__main__':
    main()