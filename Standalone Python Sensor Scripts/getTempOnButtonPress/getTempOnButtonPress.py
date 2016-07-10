import sys
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import datetime

# Note GPIO module uses Physical PIN as reference. Physical PINs are numbered in order
# Note Adafruit_DHT uses BCM PIN as reference. BCM PINs are the numbers on the breakout board.

# Setup pins for GPIO
# LED on PIN 11, or BCM PIN 17
# Button on PIN 31, or BCM PIN 6
pinLED = 11
pinButton = 31

# Setup pins for Adafruit_DHT
# Sensor on PIN 7, or BCM PIN 4
pinTempSensor = 4

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinLED, GPIO.OUT)
GPIO.setup(pinButton, GPIO.IN)

# Set initial state of LED to "off"
GPIO.output(pinLED, GPIO.HIGH)

# Create sensor. We are using the AM2302 Sensor
# sensor_args = { '11': Adafruit_DHT.DHT11,
#                 '22': Adafruit_DHT.DHT22,
#                 '2302': Adafruit_DHT.AM2302 }
sensor = Adafruit_DHT.AM2302

# Function to convert Celsious to Fahrenheit
def CelsToFahr(a):
    return ((a*1.8 + 32.0))

# Create Loop Variable
i=0

# Create file connection to local file
f = open('TempReadings', 'w')
f.write("File created at " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '\n')
f.write("Time,Temperature (F),Humidity (%),\n")

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
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pinTempSensor)
        timeStamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        # Convert to Fahrenheit
        temperature = CelsToFahr(temperature)
        # Format strings
        temperatureStr = '{0:0.1f}'.format(temperature)
        humidityStr = '{0:0.1f}'.format(humidity)
        writeString = timeStamp + ',' + temperatureStr + ',' + humidityStr
        f.write(writeString + ',\n')
        print(timeStamp + '  Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))