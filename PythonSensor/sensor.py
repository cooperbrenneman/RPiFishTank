import sys
import time
import random

from threading import Thread
from Queue import Queue

from iotHub import HubManager
import iothub_client
import iothub_client
from iothub_client import *
from iothub_client_args import *

from RandomSensor import RandomSensor
from WaterSensor import WaterSensor

import json

# HTTP options
# Because it can poll "after 9 seconds" polls will happen effectively
# at ~10 seconds.
# Note that for scalabilty, the default value of minimumPollingTime
# is 25 minutes. For more information, see:
# https://azure.microsoft.com/documentation/articles/iot-hub-devguide/#messaging
timeout = 241000
minimum_polling_time = 9

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubClient.send_event_async. 
# By default, messages do not expire.
message_timeout = 10000

receive_context = 0
avg_wind_speed = 10.0
message_count = 5
received_count = 0


# String containing Hostname, Device Id & Device Key in the format:
# "HostName=<host_name>;DeviceId=<device_id>;SharedAccessKey=<device_key>"
connection_string = "HostName=aqengine.azure-devices.net;DeviceId=kellsdesktop;SharedAccessKey=q8bcqq9BgnjOf5bdTVFjP7MX/oV0RrALTqai6qQtkHI="

# Queue(N), N represents the message buffer.  
## A higher buffer, means the sensor can continue to operate for longer if the event consumer falles behind.
## If the buffer fills up, data loss will occur.
queue = Queue(1000)
numItems = 10


# Sensor will continually write data to the Queue as it becomes available
class SensorProducer(Thread):
    
    def __init__(self, sensor):
        Thread.__init__(self)
        
        self.sensor = sensor
    
    def run(self):
        nums = range(5)
        global queue, numItems
        # For temperature and humidity sensor
        #sensorTest = SensorClass.Sensor('test','AM2302',4)
        # For water temperature sensor
        #waterSensor = WaterSensorClass.WaterSensor("DS18B20", "00152213a7ee")
        while numItems > 0:
            message = self.sensor.read()
            
            message["queue_size"] = queue.qsize()+1
            
            queue.put(message)
            print "Produced", json.dumps(message)
            
            numItems -= 1
            
            time.sleep(random.random())


class IoTHubConsumer(Thread):
    
    def __init__(self, hub_client):
        Thread.__init__(self)
        
        self.message_count = 0
        self.hub_client = hub_client
        
        print(
            "Starting the IoT Hub Python sample using protocol %s..." %
            self.hub_client.client_protocol)
    
    def run(self):
        global queue, numItems
        while numItems > 0:
            message = queue.get()
            queue.task_done()
            
            message = json.dumps(message)
            
            print "Consumed", message
            
            try:
                self.hub_client.send_event(message, {}, self.message_count)
                self.message_count += 1
            except IoTHubError as e:
                print("Unexpected error %s from IoTHub" % e)
                return
            except KeyboardInterrupt:
                print("IoTHubClient sample stopped")
            
            time.sleep(random.random())

def main(connection_string, protocol):
    
    print("\nPython %s\n" % sys.version)
    
    print("IoT Hub for Python SDK Version: %s\n" %
            iothub_client.__version__)
    
    hub_client = HubManager(connection_string, protocol)
    #sensor = RandomSensor()
    sensor = WaterSensor("DS18B20", "00152213a7ee")
    
    consumer = IoTHubConsumer(hub_client)
    producer = SensorProducer(sensor)
    
    sensor.registerConsumer(consumer)
    sensor.registerProducer(producer)
    
    sensor.start()
    

def usage():
    print("Usage: sensor.py -p <protocol> -c <connectionstring>")
    print("    protocol        : <amqp, http, mqtt>")
    print("    connectionstring: <HostName=<host_name>;DeviceId=<device_id>;SharedAccessKey=<device_key>>")

if __name__ == '__main__':
    try:
        (connection_string, protocol) = get_iothub_opt(sys.argv[1:], connection_string)
    except OptionError as o:
        print(o)
        usage()
        sys.exit(1)

    main(connection_string, protocol)
