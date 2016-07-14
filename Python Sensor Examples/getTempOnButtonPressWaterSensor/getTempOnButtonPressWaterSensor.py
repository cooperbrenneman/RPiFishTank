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

# Setup pins for GPIO
# LED on PIN 11, or BCM PIN 17
# Button on PIN 31, or BCM PIN 6
pinLED = 11
pinButton = 31

# Setup Sensor
sensor = w1thermsensor.W1ThermSensor(w1thermsensor.W1ThermSensor.THERM_SENSOR_DS18B20, "00152213a7ee")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinLED, GPIO.OUT)
GPIO.setup(pinButton, GPIO.IN)

# Set initial state of LED to "off"
GPIO.output(pinLED, GPIO.HIGH)

# Create Loop Variable
i=0

# Create file connection to local file
f = open('TempReadings', 'w')
f.write("File created at " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '\n')
f.write("Time,Temperature (F),\n")

# Create Loop to get temperature
while i == 0:
    # Read input from switch
    value = GPIO.input(pinButton)
    # If switch is released, turn light off, and do not take a reading
    if value:
        GPIO.output(pinLED, GPIO.HIGH)
    # If switch is pressed, print message, turn on light, read temperature, and print value
    else:
        print("Reading Temperature")
        GPIO.output(pinLED, GPIO.LOW)
        # Note: The time is the time in which the Raspberry Pi receives the data.
        # This means there could be delay between when the data is read from the sensor and the time stamp. 
        # For our application, this difference is negligible.
        temperature = sensor.get_temperature(w1thermsensor.W1ThermSensor.DEGREES_F)
        timeStamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        # Format strings
        writeString = timeStamp + ',' + temperature
        f.write(writeString + ',\n')
        print(timeStamp + '  Temp={0:0.1f}*'.format(temperature))