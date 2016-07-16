import datetime

class Sensor():
    
    def __init__(self, sensorName, deviceId):
        self.name = "Abstract Sensor"
        self.sensorName = str(sensorName)
        self.deviceId = str(deviceId)
    
    def read(self):
        raise NotImplemented

    def registerProducer(self, producer):
        self.producer = producer
        
    def registerConsumer(self, consumer):
        self.consumer = consumer
    
    def getCurrentTimestamp(self):
        return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    def start(self):
        if( self.producer is None or self.consumer is None ):
            raise Exception("You must register a producer thread and consumer thread.")
            return
        
        self.producer.start()
        self.consumer.start()