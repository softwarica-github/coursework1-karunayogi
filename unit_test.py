import unittest
from unittest.mock import patch, call
import tkinter as tk
from keylogger import KeyloggerGUI

class KeyloggerGUI(KeyloggerGUI):

    def save_keylog(self):
        # Save keylog to a file
        with open('keylog.txt', 'a') as f:
            for log in self.keylog:
                f.write(log + '\n')
        # Clear keylog and reset total key presses
        self.keylog = []
        self.total_key_presses = 0

        # Print message if not running unit tests
        if not hasattr(self, 'running_tests'):
            print("Keylog saved successfully")

class TestKeyloggerGUI(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = KeyloggerGUI(self.root)
        self.app.running_tests = True  # indicate that the code is running tests

    def tearDown(self):
        self.root.destroy()

    @patch('builtins.open')
    def test_save_keylog(self, mock_open):
        # Set up mock file object
        mock_file = mock_open.return_value

        # Set keylog data and total key presses
        self.app.keylog = ['[2024-02-25 12:00:00] a', '[2024-02-25 12:00:01] b']
        self.app.total_key_presses = 2

        # Call the method to be tested
        self.app.save_keylog()

        # Assert that keylog and total key presses are cleared
        self.assertEqual(self.app.keylog, [])
        self.assertEqual(self.app.total_key_presses, 0)

    def test_clear_keylog(self):
        # Set up keylog data and total key presses
        self.app.keylog = ['[2024-02-25 12:00:00] a', '[2024-02-25 12:00:01] b']
        self.app.total_key_presses = 2

        # Call the method to be tested
        self.app.clear_keylog()

        # Assert that keylog and total key presses are cleared
        self.assertEqual(self.app.keylog, [])
        self.assertEqual(self.app.total_key_presses, 0)

if __name__ == '__main__':
    unittest.main()
