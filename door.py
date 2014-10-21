#!/usr/bin/python

from libaccess.drivers import RPi
from libaccess.database import localSQLite
from libaccess import doorController

# Parameters for an RPi interface.
SQLITE_DB = "./database.db"
RFID_SERIAL_PORT = "/dev/ttyAMA0"
RFID_SERIAL_BPS = 2400

if __name__ == "__main__":

   # Initialize the door controller and its options.
   thisRPi = RPi.API(port=RFID_SERIAL_PORT, baudrate=RFID_SERIAL_BPS)
   dbHackforge = localSQLite(SQLITE_DB)
   dc = doorController(device=thisRPi, db=dbHackforge)

   # Fire up the door controller.
   dc.main_loop()
