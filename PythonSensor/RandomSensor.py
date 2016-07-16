import random
from AbstractSensor import Sensor

class RandomSensor(Sensor):
    def __init__(self):
        Sensor.__init__(self, "randomSensor", "Infinity")
        
        self.name = "Random Sensor"
        self.nums = range(100)
        
    def read(self):
        timeStamp = self.getCurrentTimestamp()
        
        return {
            "value": random.choice(self.nums),
            "timestamp": timeStamp,
            "sensor": self.name,
            "sensorName": self.sensorName,
            "deviceId": self.deviceId   
        }