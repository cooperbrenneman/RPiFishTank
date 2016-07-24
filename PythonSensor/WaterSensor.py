import w1thermsensor
import os
import TemperatureSensors
from AbstractSensor import Sensor

class WaterSensor(Sensor):

    def __init__(self,sensorName,deviceId):
        
        Sensor.__init__(self, sensorName, deviceId)
        
        self.name = "Water Temperature Sensor"
        
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        print("test1")
        sensorObj = TemperatureSensors.getSensorLibraryMapping(self.sensorName)
        print(self.sensorName)
        self.sensor = w1thermsensor.W1ThermSensor(sensorObj,self.deviceId)

    def read(self):
        # Uncomment if you want to sleep n seconds between each reading - must put value for n
        #time.sleep(n)
        # Note: The time is the time in which the Raspberry Pi receives the data.
        # This means there could be delay between when the data is read from the sensor and the time stamp. 
        # For our application, this difference is negligible.
        try:
            temperature = self.sensor.get_temperature(w1thermsensor.W1ThermSensor.DEGREES_F)
        except:
            temperature = .1
        timeStamp = self.getCurrentTimestamp()

        return {
            "value": temperature,
            "timestamp": timeStamp,
            "sensor": self.name,
            "sensorName": self.sensorName,
            "deviceId": self.deviceId   
        }

# Example Code

# Code for actual sensor
#waterSensor = WaterSensorClass.WaterSensor("DS18B20", "00152213a7ee")
#for i in range(0,5):
#    print(waterSensor.readData())
