#!/usr/bin/python

from libaccess.rrgbdl import RPi
from libaccess.database import localSQLite
from libaccess import doorController

# Parameters for an RPi interface.
SQLITE_DB = "./database.db"

if __name__ == "__main__":

   # Initialize the door controller and its options.
   dc = doorController(device=RPi.rrgbdl(), db=localSQLite(SQLITE_DB))

   # Fire up the door controller.
   dc.main_loop()
