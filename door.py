#!/usr/bin/python

# This program controls the door at the hackforge hackerspace in 
# Windsor, ON.  The logic of the door controller has been built into
# the rpi_door package.  The rpi_door package has multiple drivers 
# for various ways to communicate with LEDs, a magnetic door lock,
# a buzzer and an RFID reader.

from rpi_door.drivers.GPIO import RPiDoor

# Create a door controller that uses RPi GPIO pins to talk to the
# RFID controller and control LEDs & a buzzer.
rpi_door = RPiDoor()

# When run by itself, just call the main loop of the door controller. 
# This is where the logic is stored for how the user swipes in, what
# to do once a valid card is detected, etc.
if __name__ == "__main__":
    rpi_door.main_loop()
