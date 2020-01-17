import unittest
from client import create_presence, ans_server
from common.config import *


class TestClient(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_create_presence(self):
        self.assertEqual(create_presence()['action'], 'presence')
    def test_user_name(self):
        self.assertEqual(create_presence('Guest')['user']['account_name'], 'Guest')
    def test_server_ans(self):
        self.assertEqual(ans_server({'responce': 200}), '200: ok')
    def test_server_ans_inc_res(self):
     with self.assertRaises(ValueError):
         ans_server({'responce': 600})

if __name__ == '__main__':
    unittest.main()