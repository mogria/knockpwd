import socket
from knockpwd.Crypto import Crypto
from knockpwd.KnockRequest import KnockRequest

class KnockClient:
    """A simple Client which is able to send KnockRequests
    to the GateKeeper over UDP."""

    def __init__(self, socket_type, address_port_pair):
        self.socket_type = socket_type
        self.address_port_pair = address_port_pair

    @staticmethod
    def create_knock_request(visit_duration):
        """Create message payload for a KnockRequest."""
        return KnockRequest.create(visit_duration).to_raw()

    @staticmethod
    def create_encrypted_knock_request(visit_duration, key):
        """Create encrypted message for a KnockRequest."""
        return Crypto.encrypt(KnockClient.create_knock_request(visit_duration), key)

    def knock(self, visit_duration, key):
        """Send a knock request with the given key and
        visit duration to a GateKeeper (knockpwd server)."""
        request = KnockClient.create_encrypted_knock_request(visit_duration, key)
        with socket.socket(self.socket_type, socket.SOCK_DGRAM) as sock:
            sock.sendto(request, self.address_port_pair)
