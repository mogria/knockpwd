import unittest
import logging

from tests.GateKeeperTest import GateKeeperTest
from tests.TestCrypto import TestCrypto

def main():
    """Runs the unit test. The output is collected in unittest.log"""
    log_format_console = "%(levelname)s: %(message)s"
    log_format_logfile = "%(asctime)s |  " + log_format_console
    logging.basicConfig(filename='unittest.log',
                        level=logging.DEBUG,
                        format=log_format_logfile)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(logging.Formatter(log_format_console))
    logging.getLogger().addHandler(stream_handler)
    unittest.main()

if __name__ == '__main__':
    main()
