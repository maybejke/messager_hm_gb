import unittest
import time

from server import process_client_message


class TestServer(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_process_client_message(self):
        self.assertEqual(process_client_message({'action': 'presence', 'time': time.time(),\
                                                 'user': {'account_name': 'Guest'}}), {'responce': 200})

    def test_process_responce(self):
        self.assertEqual(process_client_message({'action': 'test_actions', }),
                         {'responce': 400, 'error': 'bad request'})

    def test_action_responce(self):
        self.assertEqual(process_client_message({'act': 'tion', 'time': time.time()}),
                         {'responce': 400, 'error': 'bad request'})


if __name__ == "__main__":
    unittest.main()
