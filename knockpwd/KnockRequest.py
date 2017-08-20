import time
import struct

class KnockRequest:
    STRUCT_FORMAT = '!qq'

    def __init__(self, knock_time, visit_duration):
        self.knock_time = knock_time
        self.visit_duration = visit_duration

    @staticmethod
    def generate_knock_time():
        """Returns the current UTC timestamp as an int."""
        return int(time.time())

    @staticmethod
    def create(visit_duration):
        """Create a new KnockRequest with the specified visit duration."""
        knock_time = KnockRequest.generate_knock_time()
        return KnockRequest(knock_time, visit_duration)

    @staticmethod
    def from_raw(raw_knock_req):
        """Create a KnockRequest from its binary representation."""
        try:
            knock_time, visit_duration = struct.unpack(KnockRequest.STRUCT_FORMAT, raw_knock_req)
            return KnockRequest(knock_time, visit_duration)
        except:
            return None

    def to_raw(self):
        """Convert this KnockRequest to a binary representation."""
        return struct.pack(KnockRequest.STRUCT_FORMAT, self.knock_time, self.visit_duration)

    def is_knock_time_valid(self, max_seconds_tolerance):
        """Checks if the knock time is near the current UTC timestamp."""
        current_time = KnockRequest.generate_knock_time()
        return abs(current_time - self.knock_time) <= max_seconds_tolerance
