#!/usr/bin/python

from drivers import RPi
from database import localSQLite


if __name__ == "__main__":

   # Initialize the door controller and its options.
   dc = doorController(driver=RPi, db=localSQLite)

   # Fire up the door controller.
   dc.main_loop()
