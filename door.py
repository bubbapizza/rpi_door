#!/usr/bin/python

from libaccess.drivers import RasPi
from libaccess import database, doorController


#### CONSTANTS ####

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
       hackf_device = RasPi.rrgbdl()
       hackf_database = database.SQLite(SQLITE_DB)
       # hackf_database = database.mySQL()

       # Initialize the standalone door controller.
       doorController.standalone.__init__(
           self, hackf_device, hackf_database)



# When run by itself, just call the main loop of the hackforge
# door controller.
if __name__ == "__main__":

    dc = hackf_door()
    dc.main_loop()
