import socket
import struct
from knockpwd.Crypto import Crypto
from knockpwd.KnockRequest import KnockRequest

class KnockClient:

    def __init__(self, socket_type, address_port_pair):
        self.socket_type = socket_type
        self.address_port_pair = address_port_pair

    @staticmethod
    def create_knock_request(visit_duration):
        return KnockRequest.create(visit_duration).to_raw()

    @staticmethod
    def create_encrypted_knock_request(visit_duration, key):
        return Crypto.encrypt(KnockClient.create_knock_request(visit_duration), key)

    def knock(self, visit_duration, key):
        request = KnockClient.create_encrypted_knock_request(visit_duration)
        with socket.socket(self.socket_type, self.SOCK_DGRAM) as s:
            socket.sendto(request, self.address_port_pair)
