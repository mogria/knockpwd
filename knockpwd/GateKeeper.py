""" The implementation of the knockpwd server.
This module is responsible for creating the UDP
socket to receive knock requests from.
"""
import socket
import sys
import logging
from threading import Event

class GateKeeper:
    """ The knockpwd server. Handles incoming data over
    UDP and passes them to the KnockRequestHandler to process them.
    """
    def __init__(self, knock_request_handler, socket_type, bind_address_port_pair):
        """ Create an instance of the knockpwd GateKeeper.
        Provide a KnockRequestHandler the type of socket to use
        and the bind address / port as a tuple."""
        self.knock_request_handler = knock_request_handler
        self.socket = socket.socket(socket_type, socket.SOCK_DGRAM)
        self.bind_address_port_pair = bind_address_port_pair

    def recvfrom_with_timeout(self):
        """ Waits for data on the UDP port for one second
        and returns a tuple of the data and the client
        address.  Both are None if no data has been
        received."""
        try:
            data, addr = self.socket.recvfrom(1)
            return (data, addr)
        except socket.timeout:
            logging.debug("recvfrom timeout")
            return (None, None)

    def run(self, stop_event=Event()):
        """ Run the UDP-Server as long as the stop event
        isn't signaled. This will process all the
        knock requests."""
        try:
            logging.info("binding to %s:%i", *self.bind_address_port_pair)
            self.socket.bind(self.bind_address_port_pair)
            self.socket.settimeout(0.1)
            while not stop_event.is_set():
                logging.debug("waiting for data")
                data, addr = self.recvfrom_with_timeout()
                if data is not None:
                    logging.debug("handling knock")
                    self.knock_request_handler.handle(data, addr)
                else:
                    logging.debug("no/invalid knock")
        except OSError:
            logging.error(*sys.exc_info())
        finally:
            logging.info("exiting")
            self.socket.close()
