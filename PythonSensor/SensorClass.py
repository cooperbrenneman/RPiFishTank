import TemperatureSensors
import RaspberryPi3PINs
import random
import datetime
import time
try:
    import Adafruit_DHT
except:
    pass

def celsToFahr(temperature):
    return((temperature*1.8) + 32.0)

class Sensor:

    def __init__(self,sensorType,partName,bcmPin):
        self.sensorType = str(sensorType)
        self.partName = str(partName)
        if RaspberryPi3PINs.checkPINInput(bcmPin):
            self.bcmPin = bcmPin
        else:
            self.bcmPin = None
        self.sensorLibrary = TemperatureSensors.getSensorLibraryMapping(self.partName)

    def readData(self):
        if self.sensorType == 'temp':
            # Note: The time is the time in which the Raspberry Pi receives the data.
            # This means there could be delay between when the data is read from the sensor and the time stamp. 
            # For our application, this difference is negligible.
            try:
                humidity, temperature = Adafruit_DHT.read_retry(self.sensorLibrary, self.bcmPin)
            except:
                temperature = random.random()*10.0+70.0
                humidity = random.random()*5.0+20.0
            timeStamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            # Convert to Fahrenheit
            temperature = celsToFahr(temperature)
            # Format strings
            temperatureStr = '{0:0.1f}'.format(temperature)
            humidityStr = '{0:0.1f}'.format(humidity)
            returnObj = {'time': timeStamp, 'temperature': temperatureStr, 'humidity': humidityStr}
            return returnObj
        elif self.sensorType == 'test':
            # Send random values back
            timeStamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            temperatureStr = str(random.random()*10+70)
            humidityStr = str(random.random()*5+50)
            returnObj = {'time': timeStamp, 'temperature': temperatureStr, 'humidity': humidityStr}
            return returnObj
        else:
            return {'time': None, 'temperature': None, 'humidity': None}

# Example Code

# Code for actual sensor
#tempSensor = Sensor('temp','AM2302',4)
#for i in range(0,5):
#    print(tempSensor.readData())

# Code for test sensor
#sensorTest = Sensor('test','AM2302',4)
#for i in range(0,5):
#    print(sensorTest.readData())
#    time.sleep(1)

