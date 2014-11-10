#
#        Copyright (C) 2014 Shawn Wilson
#        shawn@rj11.ca
#        
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This module will allow you to run a door controller using devices 
and databases provided by libaccess.  libaccess provides drivers for
RRGBDL (rfid/red/green/buzzer/door/lock-button) devices and various 
SQL databases."""

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

                # Unlock the door.
                self.device.unlock()
                self.device.buzz()

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

