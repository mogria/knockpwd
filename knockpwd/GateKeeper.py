import socket
import logging
from threading import Event

class GateKeeper:
    def __init__(self, message_handler, socket_type, bind_address_port_pair):
        self.message_handler = message_handler
        self.socket = socket.socket(socket_type, socket.SOCK_DGRAM)
        self.bind_address_port_pair = bind_address_port_pair
    
    def recvfrom_with_timeout(self):
        try:
            data, addr = self.socket.recvfrom(1)
            return (data, addr)
        except socket.timeout:
            logging.debug("recvfrom timeout")
            return (None, None)

    def run(self, stop_event=Event()):
        try:
            self.socket.bind(self.bind_address_port_pair)
            self.socket.settimeout(0.1)
            while not stop_event.is_set():
                logging.debug("recvfrom")
                data, addr = self.recvfrom_with_timeout()
                if data is not None:
                    logging.debug("handling knock")
                    self.message_handler.handle(data, addr)
                else:
                    logging.debug("no/invalid knock")
        except OSError as e:
            logging.error("", e, e.args)
        finally:
            logging.info(" exiting")
            self.socket.close()
