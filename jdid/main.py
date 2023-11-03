# main.py
import time
import sensor
import connection
import time_ms
def record_to_csv(filename, data):
    with open(filename, "a") as file:
        file.write(data + "\n")

def main():
    sensor1, default_value = sensor.setUp()
    cpt = 1
    # while True:
        csv_filename = f"{cpt}.csv"
        ir_reading, red_reading = sensor.get_data(sensor1, default_value)

        # Get the current time
        current_time = time_ms.get_time()
        # Record data to CSV
        record_to_csv(csv_filename, f"{ir_reading},{red_reading},{current_time}")

        # print("ir_reading = ", ir_reading)
        # print("red_reading = ", red_reading)
        second_check = time.localtime()[5]
        # Send data to the server every 60 seconds
        if second_check % 60 == 0:
            try: 
                connection.send_data(csv_filename)
                cpt += 1
            except OSError:
                print("Error while sending data to server")
        
        time.sleep(0.5)

if __name__ == '__main__':
    main()
