from machine import SoftI2C, Pin
from utime import sleep, ticks_diff, ticks_ms
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM, MAX30105_PULSE_AMP_LOW, MAX30105_PULSE_AMP_HIGH, MAX30105_PULSE_AMP_LOWEST
def check_wear(ir_reading, unblockedValue, isthere):
    currentDelta = ir_reading - unblockedValue
    #print ("currentDelta = ", currentDelta)
    if currentDelta > 2500 and not isthere:
        isthere = True
    elif currentDelta <2500  and isthere:
        isthere = False
    return isthere
def setUp():
    # Initialize I2C
    i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=400000)

    # Sensor instance
    sensor = MAX30102(i2c=i2c)

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
    # Set up the sensor
    sensor.setup_sensor()
    # Set the number of samples to be averaged by the chip
    SAMPLE_AVG = 1  # Options: 1, 2, 4, 8, 16, 32
    sensor.set_fifo_average(SAMPLE_AVG)
    # Set the sample rate
    SAMPLE_RATE = 400  # Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
    sensor.set_sample_rate(SAMPLE_RATE)
    sensor.set_pulse_amplitude_red(MAX30105_PULSE_AMP_MEDIUM)  # Turn off Red LED
    sensor.set_pulse_amplitude_it(MAX30105_PULSE_AMP_MEDIUM)   # Turn off IR LED
    # Take an average of IR readings at power up
    unblockedValue = 0
    i = 0
    while i < 32:
        sensor.check()
        if sensor.available():
            sensor_read = sensor.pop_ir_from_storage()  # Read the IR value
            red_reading = sensor.pop_red_from_storage()
            unblockedValue += sensor_read
        else:
            i -= 1
        i += 1
    unblockedValue //= 32
    print ("unblockedvalue = ", unblockedValue)
    return sensor,unblockedValue
def get_data(sensor, unblockedValue):
    # Main loop
    while True:
        isthere = True
        sensor.check()
        if sensor.available():
            ir_reading = sensor.pop_ir_from_storage()
            red_reading = sensor.pop_red_from_storage()
            
            #isthere = check_wear(ir_reading, unblockedValue, isthere)
            if isthere:
                return ir_reading, red_reading