from Queue import Queue
from threading import Thread
import json
import time

# Queue(N), N represents the message buffer.  
## A higher buffer, means the sensor can continue to operate for longer if the event consumer falles behind.
## If the buffer fills up, data loss will occur.
queue = Queue(1000)
numItems = 10

debug = False

class WatcherThread(Thread):

    def __init__(self, sensor):
        Thread.__init__(self)

    def run(self):
        print "Running..."

        global debug



# Sensor will continually write data to the Queue as it becomes available
class SensorProducer(Thread):
    
    def __init__(self, sensor):
        Thread.__init__(self)
        
        self.sensor = sensor
    
    def run(self):
        nums = range(5)
        global queue, numItems, debug

        while numItems > 0:
            message = self.sensor.read()
            
            message["queue_size"] = queue.qsize()+1
            message["type"] = "Reading"
            message["message"] = "Success."
            
            queue.put(message)

            if debug:
                print "Produced", json.dumps(message)
            
            time.sleep(1)


class IoTHubConsumer(Thread):
    
    def __init__(self, hub_client):
        Thread.__init__(self)
        
        self.message_count = 0
        self.hub_client = hub_client
        
        if debug:
            print(
                "Starting the IoT Hub Python sample using protocol %s..." %
                self.hub_client.client_protocol)
    
    def run(self):
        global queue, numItems, debug

        while numItems > 0:
            message = queue.get()
            queue.task_done()
            
            message = json.dumps(message)
            
            if debug:
                print "Consumed", message
            
            try:
                self.hub_client.send_event(message, {}, self.message_count)
                self.message_count += 1
            except IoTHubError as e:
                print("Unexpected error %s from IoTHub" % e)
                return
            except KeyboardInterrupt:
                print("IoTHubClient sample stopped")
            
            time.sleep(.5)