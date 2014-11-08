# Copyright (C) 2013 Windsor Hackforge
#
# This module is part of RPi Door and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from time import sleep

#### CONSTANTS ####

# Set how many seconds to wait before locking the door after the 
# push-to-lock button has been pressed.
LOCK_WAIT_TIME = 5


class stub():
    """This is a door controller class that uses devices that are 
    RRGBDL compatible.  To initialize it, you must pass it the RRGBDL
    device."""

    def __init__(self, device):

        self.device = device

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
            if self.validate_key_code(data):
                
                # Let the user know we have a good swipe.
                self.device.toggle_red_led(on=False)
                self.device.toggle_green_led(on=True)
                self.device.buzz(5000)

                # Unlock the door.
                self.device.unlock()

                sleep(1)

                # Put the swipe card lights back to defaults, then wait
                # for someone to press the lock button.
                self.device.toggle_red_led()
                self.device.toggle_green_led()
                self.check_for_lock_request()


    def check_for_lock_request(self):
        """Continuously check to see if the push-to-lock button has
        been pressed.  If so it calls the `lock` method"""
        while True:
            sleep(0.1)
            if self.device.poll_push_to_lock():
                sleep(LOCK_WAIT_TIME)
                self.device.lock()
                break


    def validate_key_code(self, data):
        """This method would normally be overridden with a custom
        authentication mechanism.  As it is now, it just returns
        True no matter what is passed to it."""
        
        return True



class standalone(stub):
    """This door controller has all the basic door controls along with a 
    standalone user database used for key validation."""

    def __init__(self, device, database):
        """To initialize the stadalone door controller, you must pass
        it a libaccess database object along w/ the device."""

        super().__init__(device)
        self.db = database


    def validate_key_code(self, data):
        """Check the key code against the libaccess user database."""

        self.db.checkAuth(data)

