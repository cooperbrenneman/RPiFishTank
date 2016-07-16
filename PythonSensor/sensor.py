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
connection_string = "HostName=aquariumstream.azure-devices.net;DeviceId=windowspythontest;SharedAccessKey=N4qipAx2G4v/J+vLMt6iIYNRvTk6xHLyxDrrU4wuTrI="

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
        while numItems > 0:
            
            reading = self.sensor.read()
            
            message = {
                "sensor_name": self.sensor.name,
                "sensor_value": reading,
                "queue_size": queue.qsize()+1
            }
            
            queue.put(message)
            print "Produced", json.dumps(message)
            
            numItems -= 1
            
            time.sleep(random.random())


class IoTHubConsumer(Thread):
    
    def __init__(self, sensor):
        Thread.__init__(self)
        
        self.sensor = sensor
        self.message_count = 0
        
        self.sensor.hub_manager = HubManager(connection_string, protocol)
        print(
            "Starting the IoT Hub Python sample using protocol %s..." %
            self.sensor.hub_manager.client_protocol)
    
    def run(self):
        global queue, numItems
        while numItems > 0:
            message = queue.get()
            queue.task_done()
            
            message = json.dumps(message)
            
            print "Consumed", message
            
            try:
                self.sensor.hub_manager.send_event(message, {}, self.message_count)
                self.message_count += 1
            except IoTHubError as e:
                print("Unexpected error %s from IoTHub" % e)
                return
            except KeyboardInterrupt:
                print("IoTHubClient sample stopped")
            
            time.sleep(random.random())


class Sensor():
    
    def __init__(self, connection_string, protocol):
        self.name = "Abstract Sensor"
        
        self.connection_string = connection_string
        self.protocol = protocol
        
        self.hub_manager = HubManager(connection_string, protocol)
        
        self.producer = SensorProducer(self)
        self.consumer = IoTHubConsumer(self)
    
    
    def read(self):
        raise NotImplemented
        
        
    def start(self):
        self.producer.start()
        self.consumer.start()
        
        
        
class RandomSensor(Sensor):
    def __init__(self, connection_string, protocol):
        Sensor.__init__(self, connection_string, protocol)
        
        self.name = "Random Sensor"
        
        self.nums = range(100)
        
    def read(self):
        return random.choice(self.nums)

def main(connection_string, protocol):
    
    print("\nPython %s\n" % sys.version)
    
    print("IoT Hub for Python SDK Version: %s\n" %
            iothub_client.__version__)
    
    sensor = RandomSensor(connection_string, protocol)
    sensor.start()
    
    '''SensorProducer().start()
    IoTHubConsumer(connection_string, protocol).start()'''
    
    '''try:
        print("\nPython %s\n" % sys.version)
        print(
            "IoT Hub for Python SDK Version: %s\n" %
            iothub_client.__version__)

        hub_manager = HubManager(connection_string, protocol)

        print(
            "Starting the IoT Hub Python sample using protocol %s..." %
            hub_manager.client_protocol)


        while True:
            # send a few messages every minute
            print("IoTHubClient sending %d messages" % message_count)

            for i in range(0, message_count):
                msg_txt_formatted = msg_txt % (
                    avg_wind_speed + (random.random() * 4 + 2))
                msg_properties = {
                    "Property": "PropMsg_%d" % i
                }
                hub_manager.send_event(msg_txt_formatted, msg_properties, i)
                print(
                    "IoTHubClient.send_event_async accepted message [%d]"
                    " for transmission to IoT Hub." %
                    i)

            # Wait for Commands or exit
            print("IoTHubClient waiting for commands, press Ctrl-C to exit")

            n = 0
            while n < 1:
                status = hub_manager.client.get_send_status()
                print("Send status: %s" % status)
                time.sleep(10)
                n += 1

    except IoTHubError as e:
        print("Unexpected error %s from IoTHub" % e)
        return
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")'''


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
