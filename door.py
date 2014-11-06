#!/usr/bin/python

from libaccess.drivers import RPi
from libaccess.database import localSQLite
from libaccess import doorController


#### CONSTANTS ####

# Set up specifics for the hackforge door controller.

SQLITE_DB = "./database.db"

class hackf_door(doorController, localSQLite):
    """This is the hackforge door controller.  It uses a Raspberry
    Pi for the RRGBDL device, along with a local SQLite database for
    authenticating RFID cards."""

    def __init__(self):
        """Set up the RPi device and the authentication database."""

       raise NotImplementedError("Not implemented")



# When run by itself, just call the main loop of the door controller. 
if __name__ == "__main__":

   dc = hackf_door()
   dc.main_loop()
