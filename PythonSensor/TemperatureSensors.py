# Temperature Sensors module to check validity of Sensors
# Module only available on Raspberry Pi. Try Except needed to test on client
try:
    import Adafruit_DHT
except:
    pass
import w1thermsensor

# Since Adafruit_DHT module is only available on Raspberry Pi, use strings on client for testing.
try:
    temperatureSensorsDict = {
                              "DS1822" : w1thermsensor.W1ThermSensor.THERM_SENSOR_DS1822,
                              "DS18B20" : w1thermsensor.W1ThermSensor.THERM_SENSOR_DS18B20,
                              "DS18S20" : w1thermsensor.W1ThermSensor.THERM_SENSOR_DS18S20}
except Exception as e:
    print(str(e))
    temperatureSensorsDict = {"DHT11": 'Adafruit_DHT.DHT11',
                              "DHT22" : 'Adafruit_DHT.DHT22',
                              "AM2302" : 'Adafruit_DHT.AM2302'}

# Return keys in dictionary
def getNames():
    return temperatureSensorsDict.keys()

# Return sensor object from dictionary
def getSensorLibraryMapping(sensorName):
    if(sensorName in getNames()):
        return temperatureSensorsDict[sensorName]
    else:
        print(str(sensorName) + " sensor name does not exist in library mapping.")
        print(str(temperatureSensorsDict))
        return None


