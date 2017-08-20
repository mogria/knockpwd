from knockpwd.Crypto import Crypto
import struct

class KnockRequestHandler:
    TIME_TOLERANCE_SECONDS = 30 # half a minute
    MAX_VISIT_DURATION_SECONDS = 10 * 60 # ten minutes

    def __init__(self, key):
        if len(key) != Crypto.KEY_SIZE:
            raise ValueError("At least a key size of 16 bytes is required")
        self.key = key

    def check_knock_time(self, knock_request):
        return knock_request.is_knock_time_valid(KnockRequestHandler.TIME_TOLERANCE_SECONDS)

    def check_visit_duration(self, knock_request):
        return knock_request.visit_duration < KnockRequestHandler.MAX_VISIT_DURATION_SECONDS 

    def parse(self, data):
        return KnockRequest.from_raw(data)

    def validate(self, knock_request):
        return self.check_knock_time(knock_request) and self.check_visit_duration(knock_request)

    def execute(self, knock_request):
        pass

    def handle(self, data, addr):
        decrypted_data = Crypto.decrypt(data)
        if decrypted_data is None:
            return None

        knock_request = self.parse(decrypted_data)
        if not self.validate(knock_request):
            return None

        return self.execute(knock_request)

        


