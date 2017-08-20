from knockpwd.KnockRequestHandler import KnockRequestHandler
from knockpwd.KnockRequest import KnockRequest
from knockpwd.Crypto import Crypto
from nose.tools import assert_is_none, assert_true, assert_false, assert_raises

class TestKnockRequestHandler:

    def setUp(self):
        self.handler = KnockRequestHandler(Crypto.generate_key())
        self.req_invalid_knock_time = KnockRequest(0, 100)
        self.req_invalid_visit_duration = KnockRequest(0, 1000000)
        self.request_valid = KnockRequest.create(100)

    def tearDown(self):
        pass

    def test_invalid_key(self):
        assert_raises(ValueError, KnockRequestHandler, Crypto.generate_key()[:-1])

    def test_parse_garbage(self):
        assert_is_none(self.handler.parse(b"complete and utter garbage"))

    def test_validate(self):
        assert_true(self.handler.validate(self.request_valid))

    def test_validate_invalid_knock_time(self):
        assert_false(self.handler.validate(self.req_invalid_knock_time))

    def test_validate_invalid_visit_duration(self):
        assert_false(self.handler.validate(self.req_invalid_visit_duration))
