import threading
from coapthon.client.helperclient import HelperClient

import logging
log = logging.getLogger("MoteObserving")


class StartObserve(threading.Thread):
    def __init__(self, host, path, port=5683, is_observer=False, group=None, target=None, name=None, kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.coap_client = None
        self.kwargs = kwargs
        self.host = host
        self.path = path
        self.port = port
        self.is_observer = is_observer
        return

    def message_callback(self, response):
        """
        :type response: coapthon.messages.response.Response
        """
        if response is not None:
            log.debug("Got new message")
            if log.isEnabledFor(logging.DEBUG):
                packet_content = ":".join("{:02x}".format(ord(c)) for c in response.payload)
                log.debug(packet_content)
            #log.debug("Payload length: {0}".format(len(response.payload)))

            log.debug("=================================")

    def run(self):
        log.info("MoteConnector \"{0}\" started.".format(self.name))
        self.coap_client = HelperClient(server=(self.host, self.port))
        if self.is_observer:
            self.coap_client.observe(path=self.path, callback=self.message_callback)
        else:
            self.coap_client.get(path=self.path, callback=self.message_callback)
        return

    def close(self):
        log.info("Closing MoteConnector \"{0}\".".format(self.name))
        if self.coap_client is not None:
            self.coap_client.stop()