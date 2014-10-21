#!/usr/bin/python

from libaccess.drivers import RPi
from libaccess.database import localSQLite
from libaccess import doorController


if __name__ == "__main__":

   # Initialize the door controller and its options.
   dc = doorController(driver=RPi, db=localSQLite)

   # Fire up the door controller.
   dc.main_loop()
