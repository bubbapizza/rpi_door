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


class hackf_door(doorController.standalone):
    """This is the hackforge door controller.  It uses a Raspberry
    Pi for the RRGBDL device, along with a local SQLite database for
    authenticating RFID cards."""

    def __init__(self):
        """Set up the RPi device and the authentication database."""

       # Set up the details of the door controller device and the 
       # database.
       hackf_device = RPi.rrgbdl(
           port=PORT, 
           baudrate=BAUD_RATE,
           red = RED,
           green = GREEN,
           buzzer = BELL,
           door = DOOR,
           button = LOCK_BUTTON
       )
       hackf_database = localSQLite(SQLITE_DB)


       # Initialize the standalone door controller.
       super().__init__(hackf_device, hackf_database)




# When run by itself, just call the main loop of the hackforge
# door controller.
if __name__ == "__main__":

   dc = hackf_door()
   dc.main_loop()
