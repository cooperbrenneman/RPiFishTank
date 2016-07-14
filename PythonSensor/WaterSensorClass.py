import datetime
import time
import w1thermsensor
import os
import TemperatureSensors

class WaterSensor:

    def __init__(self,partName,deviceId):
        self.partName = str(partName)
        self.deviceId = str(deviceId)
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        sensorObj = TemperatureSensors.getSensorLibraryMapping(self.partName)
        self.sensor = w1thermsensor.W1ThermSensor(sensorObj,self.deviceId)

    def readData(self):
        # Uncomment if you want to sleep n seconds between each reading - must put value for n
        #time.sleep(n)
        # Note: The time is the time in which the Raspberry Pi receives the data.
        # This means there could be delay between when the data is read from the sensor and the time stamp. 
        # For our application, this difference is negligible.
        try:
            temperature = self.sensor.get_temperature(w1thermsensor.W1ThermSensor.DEGREES_F)
        except:
            temperature = .1
        timeStamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        # Return object
        return {'time': timeStamp, 'temperature': temperature}

# Example Code

# Code for actual sensor
#waterSensor = WaterSensorClass.WaterSensor("DS18B20", "00152213a7ee")
#for i in range(0,5):
#    print(waterSensor.readData())