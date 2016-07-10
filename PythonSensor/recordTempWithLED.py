import sys
import time
import Adafruit_DHT
import RPi.GPIO as GPIO

pinLED = 5                             ## We're working with pin 5
GPIO.setmode(GPIO.BOARD)               ## Use BOARD pin numbering
GPIO.setup(pinLED, GPIO.OUT)           ## Set pin 5 to OUTPUT

sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
sensor = Adafruit_DHT.AM2302
pin = 4

    ##Function to convert celsius to fahrenheit
def CToF(a):
    return ((a*1.8 + 32.0))
i=0
##Create loop to always grab temperature
while i == 0:
    GPIO.output(pinLED, GPIO.HIGH)
    time.sleep(5)
# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    GPIO.output(pinLED, GPIO.LOW)
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temperature = CToF(temperature)

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
        i = 1
        sys.exit(1)

GPIO.cleanup()