import sys
import time
import RPi.GPIO as GPIO
import datetime
import w1thermsensor
import os

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Note GPIO module uses Physical PIN as reference. Physical PINs are numbered in order
# Note Adafruit_DHT uses BCM PIN as reference. BCM PINs are the numbers on the breakout board.

# Setup Sensor
sensor = w1thermsensor.W1ThermSensor(w1thermsensor.W1ThermSensor.THERM_SENSOR_DS18B20, "00152213a7ee")

# Create Loop to get temperature
while True:
    # Uncomment if you want to sleep n seconds between each reading - must put value for n
    #time.sleep(n)
    # Note: The time is the time in which the Raspberry Pi receives the data.
    # This means there could be delay between when the data is read from the sensor and the time stamp. 
    # For our application, this difference is negligible.
    temperature = sensor.get_temperature(w1thermsensor.W1ThermSensor.DEGREES_F)
    timeStamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    # Format strings
    print(timeStamp + ' ' + str(temperature))