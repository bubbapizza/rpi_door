#!/usr/bin/python

from libaccess.drivers import RPi
from libaccess.database import localSQLite
from libaccess import doorController


#### CONSTANTS ####

# Broadcom GPIO pin numbers for switches/buzzer.
RED = 24
GREEN = 23
DOOR = 25
BELL = 18
LOCK_BUTTON = 17

# Serial port settings
PORT = "/dev/ttyAMA0"
BAUD_RATE = 2400
RFID_DEFAULT_TIMEOUT = 5

# Here's the database where user credentials are stored.
SQLITE_DB = "./database.db"


class hackf_door(doorController, localSQLite):
    """This is the hackforge door controller.  It uses a Raspberry
    Pi for the RRGBDL device, along with a local SQLite database for
    authenticating RFID cards."""

    def __init__(self):
        """Set up the RPi device and the authentication database."""

       # Create an RRGBDL device for controlling the door and initialize
       # the doorController class.
       hackf_dev = RPi.rrgbdl(
           port=PORT, 
           baudrate=BAUD_RATE,
           red = RED,
           green = GREEN,
           buzzer = BELL,
           door = DOOR,
           button = LOCK_BUTTON
       )
       doorController.__init__(self, hackf_dev)

       # Set up a database for the door controller.
       localSQLite.__init__(self, SQLITE_DB)



# When run by itself, just call the main loop of the door controller. 
if __name__ == "__main__":

   dc = hackf_door()
   dc.main_loop()
