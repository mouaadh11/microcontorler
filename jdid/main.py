# main.py
import time
#import sensor
#import connection


def main():
   sensor1, default_value = sensor.setUp()
   cpt = 0
   while True:
        cpt += 1
        ir_reading, red_reading = sensor.get_data(sensor1, default_value)
        current_time = str(time.localtime()[3] +1) + ":" + str(time.localtime()[4]) + ":" + str(time.localtime()[5])
        try:
            connection.send_data(ir_reading, red_reading, cpt, current_time)
        except OSError:
            print("Error while sending data to server")
        print("ir_reading = ", ir_reading)
        print("red_reading = ", red_reading)
        time.sleep(0.5)

if __name__ == '__main__':
    main()