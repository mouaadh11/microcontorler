# # main.py
import time
# import sensor
import connection
import time_ms
# def record_to_csv(filename, data):
#     with open(filename, "a") as file:
#         file.write(data + "\n")

# def main():
#     sensor1, default_value = sensor.setUp()
#     cpt = 1
#     start_recording = time.ticks_ms()
#     print ("start_recording", start_recording)
#     csv_filename = "wrist_MED_2.csv"
#     with open(csv_filename, "a") as file:
#         file.write("hr,red,datetime\n")
#     while True:
        
#         ir_reading, red_reading = sensor.get_data(sensor1, default_value)
#         # Get the current time
#         current_time = time_ms.get_time()
#         # Record data to CSV
#         record_to_csv(csv_filename, f"{ir_reading},{red_reading},{current_time}")

#         #print("ir_reading = ", ir_reading)
#         #print("red_reading = ", red_reading)
#         #second_check = time.localtime()[5]
#         #print(time.ticks_diff(time.ticks_ms(), start_recording))
#         # Send data to the server every 60 seconds
#         if time.ticks_diff(time.ticks_ms(), start_recording) >= 60000:
#             start_recording = time.ticks_ms()
#             print ("dkhalt")
#             try: 
#                 connection.send_data(csv_filename)
#                 cpt += 1
#             except OSError:
#                 print("Error while sending data to server")
#             return 0
            
#             #time.sleep(0.5)

# if __name__ == '__main__':
#     main()
import time
import connection
import time_ms
import uos
from machine import sleep, SoftI2C, Pin
from utime import ticks_diff, ticks_us
import gc
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM

# main.py
# gc.enable()
def main():
    csv_filename = "samples-try.csv"
    with open(csv_filename, "a") as file:
        file.write("hr,red,datetime\n")
    # I2C software instance
    i2c = SoftI2C(sda=Pin(21),  # Here, use your I2C SDA pin
                  scl=Pin(22),  # Here, use your I2C SCL pin
                  freq=400000)  # Fast: 400kHz, slow: 100kHz

    # Examples of working I2C configurations:
    # Board             |   SDA pin  |   SCL pin
    # ------------------------------------------
    # ESP32 D1 Mini     |   22       |   21
    # TinyPico ESP32    |   21       |   22
    # Raspberry Pi Pico |   16       |   17
    # TinyS3			|	 8		 |    9

    # Sensor instance
    sensor = MAX30102(i2c=i2c)  # An I2C instance is required

    # Scan I2C bus to ensure that the sensor is connected
    if sensor.i2c_address not in i2c.scan():
        print("Sensor not found.")
        return
    elif not (sensor.check_part_id()):
        # Check that the targeted sensor is compatible
        print("I2C device ID not corresponding to MAX30102 or MAX30105.")
        return
    else:
        print("Sensor connected and recognized.")

    # It's possible to set up the sensor at once with the setup_sensor() method.
    # If no parameters are supplied, the default config is loaded:
    # Led mode: 2 (RED + IR)
    # ADC range: 16384
    # Sample rate: 400 Hz
    # Led power: maximum (50.0mA - Presence detection of ~12 inch)
    # Averaged samples: 8
    # pulse width: 411
    print("Setting up sensor with default configuration.", '\n')
    sensor.setup_sensor()

    sleep(1)

    # The readTemperature() method allows to extract the die temperature in °C    
    print("Reading temperature in °C.", '\n')
    print(sensor.read_temperature())

    # Select whether to compute the acquisition frequency or not
    compute_frequency = True

    print("Starting data acquisition from RED & IR registers...", '\n')
    sleep(1)

    readings_list_total = [[None, None, None] for i in range(1100)]
    cpt = 0
    t_start = ticks_us()  # Starting time of the acquisition
    start_recording = time.ticks_ms()
    samples_n = 0  # Number of samples that have been collected

    while True:
        # The check() method has to be continuously polled, to check if
        # there are new readings into the sensor's FIFO queue. When new
        # readings are available, this function will put them into the storage.
        sensor.check()

        # Check if the storage contains available samples
        if sensor.available():
            # print ("(before writing) the free memory is: ", gc.mem_free(), "bytes")

            # Access the storage FIFO and gather the readings (integers)
            
            red_reading = sensor.pop_red_from_storage()
            ir_reading = sensor.pop_ir_from_storage()
            
            # Get the current time
            current_time = time_ms.get_time()
            
            readings_list_total[cpt][0]= red_reading
            readings_list_total[cpt][1]= ir_reading
            readings_list_total[cpt][2]= current_time
            cpt = cpt + 1
            # Compute the real frequency at which we receive data
            if compute_frequency:
                if ticks_diff(ticks_us(), t_start) >= 999999:
                    f_HZ = samples_n
                    samples_n = 0
                    print("acquisition frequency = ", f_HZ)
                    t_start = ticks_us()
                else:
                    samples_n = samples_n + 1

            if time.ticks_diff(time.ticks_ms(), start_recording) >= 20000:
                print ("dkhalt")
                #print (readings_list_total)
                with open(csv_filename, "a") as file:
                     for i in range(cpt):
                        file.write( f"{readings_list_total[i][1]},{readings_list_total[i][0]},{readings_list_total[i][2]}"+ '\n')
                cpt = 1
                gc.collect()
                uos.remove(csv_filename)
                start_recording = time.ticks_ms()
                #print(readings_list_total)
                #send data to server


if __name__ == '__main__':
    main()
    