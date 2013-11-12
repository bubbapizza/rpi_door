#!/usr/bin/python
#
#        Copyright (C) 2013 Randy Topliffe, Shawn Wilson
#        randytopliffe@gmail.com
#        shawn@ch2a.ca
#
#        
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   This program was written by Randy Topliffe with comments added by
#   Shawn Wilson 


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
