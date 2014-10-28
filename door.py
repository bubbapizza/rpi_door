#!/usr/bin/python

from libaccess.rrgbdl import RPi
from libaccess.database import localSQLite
from libaccess import doorController

# Parameters for an RPi interface.
SQLITE_DB = "./database.db"

# When run by itself, just call the main loop of the door controller. 
# This is where the logic is stored for how the user swipes in, what
# to do once a valid card is detected, etc.
if __name__ == "__main__":

   # Initialize the door controller and its options.
   dc = doorController(device=RPi.rrgbdl(), db=localSQLite(SQLITE_DB))

   # Fire up the door controller.
   dc.main_loop()
