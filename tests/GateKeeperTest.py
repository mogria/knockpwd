import logging
import socket
import time
from threading import Thread, Event
import unittest
from unittest.mock import Mock


import knockpwd

class GateKeeperTest(unittest.TestCase):

    def setUp(self):
        self.socket_type = socket.AF_INET
        self.bind_address_port_pair = ("127.0.0.1", 46589)
        self.message_handler = Mock(spec_set=knockpwd.MessageHandler.MessageHandler)
        self.gate_keeper = knockpwd.GateKeeper.GateKeeper(self.message_handler, self.socket_type, self.bind_address_port_pair)
        self.thread_stopper_event = Event()
        self.thread = None

    def start_server(self):
        self.thread = Thread(target=self.gate_keeper.run, args=(self.thread_stopper_event,))
        self.thread.start()

    def tearDown(self):
        if self.thread is not None:
            self.thread_stopper_event.set()
            self.thread.join()

    """Helper method for sending an UDP knock."""
    def send_knock(self):
        s = socket.socket(self.socket_type, socket.SOCK_DGRAM)
        s.sendto(b"foo", self.bind_address_port_pair)
        s.close()

    """Check if the server starts processing a knock at all."""
    def test_run(self):
        self.start_server()
        self.send_knock()
        time.sleep(0.1)
        self.message_handler.handle.assert_called_once()

    """Check if the server processes multiple knocks."""
    def test_run_twice(self):
        self.start_server()
        num_knocks = 10
        for i in range(num_knocks):
            time.sleep(0.1)
            self.send_knock()

        time.sleep(0.1)
        self.assertEqual(num_knocks, self.message_handler.handle.call_count, 'Not all knocks were handled by the MessageHandler')

    """Check behavior when udp address/port is already in use."""
    def test_fail_to_bind(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(self.bind_address_port_pair)

        # temporarily disable logging, because
        # there should be an error, and this is
        # confusing in the test output
        logging.disable(logging.CRITICAL)

        self.start_server()
        time.sleep(0.1)

        sock.close()
        logging.disable(logging.NOTSET)

        self.assertFalse(self.thread.is_alive())
