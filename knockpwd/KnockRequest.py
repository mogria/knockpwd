import time
import struct

class KnockRequest:
    STRUCT_FORMAT = '!qq'

    def __init__(self, knock_time, visit_duration):
        self.knock_time = knock_time
        self.visit_duration = visit_duration

    @staticmethod
    def generate_knock_time():
        return int(time.time())

    @staticmethod
    def create(visit_duration):
        knock_time = KnockRequest.generate_knock_time()
        return KnockRequest(knock_time, visit_duration)

    @staticmethod
    def from_raw():
        return KnockRequest(*struct.unpack(KnockRequest.STRUCT_FORMAT, raw_knock_request))

    def to_raw(self):
        return struct.pack(KnockRequest.STRUCT_FORMAT, self.knock_time, self.visit_duration)

    def is_knock_time_valid(self, max_seconds_tolerance):
        current_time = KnockRequest.generate_knock_time()
        return abs(curret_time - self.knock_time) <= max_seconds_tolerance
