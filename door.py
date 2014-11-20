#!/usr/bin/python

from libaccess.drivers import RPi
from libaccess import database, doorController


#### CONSTANTS ####

# Override the buzzer pin for the RPi since we're using a rev2 RPi.
# For all the other RPi driver settings, just use the defaults.
RPI_REV2_BELL = 27

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
       hackf_device = RPi.rrgbdl(buzzer = RPI_REV2_BELL)
       hackf_database = database.SQLite(SQLITE_DB)

       # Initialize the standalone door controller.
       doorController.standalone.__init__(hackf_device, hackf_database)



# When run by itself, just call the main loop of the hackforge
# door controller.
if __name__ == "__main__":

   dc = hackf_door()
   dc.main_loop()
