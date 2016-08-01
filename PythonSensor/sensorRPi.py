import sys

from iotHub import HubManager
import iothub_client
from iothub_client import *
from iothub_client_args import *

from RandomSensor import RandomSensor
from WaterSensor import WaterSensor

from SensorThreadLayer import IoTHubConsumer, SensorProducer, WatcherThread


# Turns on verbose messaging
debug = False

# String containing Hostname, Device Id & Device Key in the format:
# "HostName=<host_name>;DeviceId=<device_id>;SharedAccessKey=<device_key>"
connection_string = "HostName=aqengine.azure-devices.net;DeviceId=raspi;SharedAccessKey=I5Qfa/ZPbZRGjSsEmazrv6N8MGY6DKoURTYy59JjCiE="


def main(connection_string, protocol):
    
    print("\nPython %s\n" % sys.version)
    
    print("IoT Hub for Python SDK Version: %s\n" %
            iothub_client.__version__)
    
    hub_client = HubManager(connection_string, protocol)
    #sensor = RandomSensor()
    sensor = WaterSensor("DS18B20", "00152213a7ee") # Only run this on the raspberry PI
    
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
