import time
import struct
import socket

from knockpwd.KnockClient import KnockClient
from knockpwd.KnockRequest import KnockRequest
from knockpwd.Crypto import Crypto
from nose.tools import assert_equals, assert_is_not_none

class TestKnockClient:

    def setUp(self):
        self.key = Crypto.generate_key()
        self.addr_port_pair = ('127.0.0.1', 35341)
        self.client = KnockClient(socket.AF_INET, self.addr_port_pair)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(self.addr_port_pair)
        self.expected_time = int(time.time())

    def tearDown(self):
        self.server.close()
    
    def check_knock_request(self, raw_knock_request, expected_visit_duration):
        knock_request = KnockRequest.from_raw(raw_knock_request)
        assert_equals(self.expected_time, knock_request.knock_time)
        assert_equals(expected_visit_duration, knock_request.visit_duration)

    def test_create_knock_request(self):
        expected_visit_duration = 601
        knock_request = KnockClient.create_knock_request(expected_visit_duration)
        self.check_knock_request(knock_request, expected_visit_duration)
        
    def test_create_encrypted_knock_request(self):
        expected_visit_duration = 12600
        KnockClient.create_encrypted_knock_request
        encrypted_knock_request = KnockClient.create_encrypted_knock_request(expected_visit_duration, self.key)
        knock_request = Crypto.decrypt(encrypted_knock_request, self.key)
        assert_is_not_none(knock_request)
        self.check_knock_request(knock_request, expected_visit_duration)

    def test_knock(self):
        expected_visit_duration = 111
        self.client.knock(expected_visit_duration, self.key)
        data, addr = self.server.recvfrom(2048)
        assert_is_not_none(data)
        decrypted = Crypto.decrypt(data, self.key)
        assert_is_not_none(decrypted)
        self.check_knock_request(decrypted, expected_visit_duration)

