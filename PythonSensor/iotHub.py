import random
import time
import sys
import iothub_client
from iothub_client import *
from iothub_client_args import *

# global counters
receive_callbacks = 0
send_callbacks = 0
blob_callbacks = 0

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubClient.send_event_async. 
# By default, messages do not expire.
message_timeout = 10000

receive_context = 0

class HubManager(object):

    def __init__(
            self,
            connection_string,
            protocol=IoTHubTransportProvider.AMQP):
        self.client_protocol = protocol
        self.client = IoTHubClient(connection_string, protocol)
        if protocol == IoTHubTransportProvider.HTTP:
            self.client.set_option("timeout", timeout)
            self.client.set_option("MinimumPollingTime", minimum_polling_time)
        # set the time until a message times out
        self.client.set_option("messageTimeout", message_timeout)
        # some embedded platforms need certificate information
        # self.set_certificates()
        self.client.set_message_callback(self._receive_message_callback, receive_context)

    def set_certificates(self):
        from iothub_client_cert import certificates
        try:
            self.client.set_option("TrustedCerts", certificates)
            print("set_option TrustedCerts successful")
        except IoTHubClientError as e:
            print("set_option TrustedCerts failed (%s)" % e)

    def _receive_message_callback(self, message, counter):
        global receive_callbacks
        buffer = message.get_bytearray()
        size = len(buffer)
        print("Received Message [%d]:" % counter)
        print("    Data: <<<%s>>> & Size=%d" %
              (buffer[:size].decode('utf-8'), size))
        map_properties = message.properties()
        key_value_pair = map_properties.get_internals()
        print("    Properties: %s" % key_value_pair)
        counter += 1
        receive_callbacks += 1
        print("    Total calls received: %d" % receive_callbacks)
        return IoTHubMessageDispositionResult.ACCEPTED

    def _send_confirmation_callback(self, message, result, user_context):
        global send_callbacks
        print(
            "Confirmation[%d] received for message with result = %s" %
            (user_context, result))
        map_properties = message.properties()
        key_value_pair = map_properties.get_internals()
        print("    Properties: %s" % key_value_pair)
        send_callbacks += 1
        print("    Total calls confirmed: %d" % send_callbacks)


    def _blob_upload_confirmation_callback(self, result, user_context):
        global blob_callbacks
        print("Blob upload confirmation[%d] received for message with result = %s" % (user_context, result))
        blob_callbacks += 1
        print("    Total calls confirmed: %d" % blob_callbacks)


    def send_event(self, event, properties, send_context):
        if not isinstance(event, IoTHubMessage):
            event = IoTHubMessage(bytearray(event, 'utf8'))

        if len(properties) > 0:
            prop_map = event.properties()
            for key in properties:
                prop_map.add_or_update(key, properties[key])

        self.client.send_event_async(
            event, self._send_confirmation_callback, send_context)


    def upload_to_blob(self, destinationfilename, source, size, usercontext):
        self.client.upload_blob_async(
            destinationfilename, source, size,
            self._blob_upload_confirmation_callback, usercontext)