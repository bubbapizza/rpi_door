# Copyright (C) 2013 Windsor Hackforge
#
# This module is part of RPi Door and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import re
from time import sleep


class doorController():

    code_re = re.compile("\\n(.+)\\r", re.UNICODE)

    def __init__(self, device, db):

        self.device = device
        self.db = db

        # Makes sure the state of the door is locked when first started. This
        # is mostly for security reasons. For example, if the power goes out we
        # want to door to lock when the power comes back on. Trying to remember
        # the door's state in should events would be difficult and not worth
        # the effort.
        self.device.lock()
        self.device.toggle_red_led(on=True)

    def main_loop(self):
        while True:

            # Wait for someone to swipe an RFID card.
            data = self.device.read_RFID()

            # If we got a valid authentication, then unlock the door.
            if data and self.validate_key_code(data):
                
                # Let the user know we have a good swipe.
                self.toggle_red_led(on=False)
                self.toggle_green_led(on=True)
                self.buzz(5000)

                # Unlock the door.
                self.unlock()

                sleep(1)

                # Put the swipe card lights back to defaults, then wait
                # for someone to press the lock button.
                self.toggle_red_led()
                self.toggle_green_led()
                self.check_for_lock_request()

    def find_key_code(self, data):
        """ Checks the given string to see if it contains a code (valid or not)

        Args:
            data (str): data to be checked

        Returns:
            None or str::
                None if there isn't a match or the code if there is a match

        """
        match = re.match(self.code_re, data)
        if match:
            return match.groups()[0]
        return None


    def check_for_lock_request(self):
        """Continuously check to see if the state is true. If so, call the
        `lock` method
        """
        while True:
            sleep(0.1)
            if self.get_state():
                sleep(5)
                self.lock()
                break

    def get_state(self):
        raise NotImplementedError("Not implemented.")

    def validate_key_code(self, data):
        raise NotImplementedError("Not implemented.")

    def unlock(self):
        raise NotImplementedError("Not implemented.")

    def lock(self):
        raise NotImplementedError("Not implemented.")

    def toggle_red_led(self, on=False):
        raise NotImplementedError("Not implemented.")

    def toggle_green_led(self, on=False):
        raise NotImplementedError("Not implemented.")
