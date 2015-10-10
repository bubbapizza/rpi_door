#!/usr/bin/python
#
#        Copyright (C) 2014 Shawn Wilson
#        shawn@rj11.ca
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


"""This is a hardware device driver for the door controller using a
Raspberry Pi's GPIO pins and serial port.  

It implements an RRGBDL (rfid/red/green/buzzer/door/lock-button)
hardware API that the door controller uses.  The RRGBDL API has nothing
to do with anything and is just an arbitrary API that I made up.

By default, the RRGBDL assumes we're using an RDM6300 RFID reader
and a raspberry pi v2.

TODO: 
   * specify RPi version in RRGBDL API
   * abstract out RFID drivers."""



import serial
import time
import switch

#### CONSTANTS ####

## Set up 125khz RFID ##

# These values are specifically for the Parallax 28140 serial
# RFID reader as described at http://www.parallax.com/product/28140
#
# RFID_NUM_BYTES = 10
# RFID_START_BYTE = 10
# RFID_STOP_BYTE = 13

# These values are for those cheap RDM6300 readers that you can find 
# all over ebay.
RFID_NUM_BYTES = 12
RFID_START_BYTE = 2
RFID_STOP_BYTE = 3


## Set up default values for the RPi ##

# Broadcom GPIO pin numbers for switches/buzzer.
RED = 24
GREEN = 23
DOOR = 25
# BELL = 21  # For RPi rev 1
BELL = 27  # For RPi rev 2
LOCK_BUTTON = 17

# Serial port settings
PORT = "/dev/ttyAMA0"
BAUD_RATE = 2400
RFID_DEFAULT_TIMEOUT = 5



class SerialConnectionError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class rrgbdl():
    """ This is an rfid/red/green/buzzer/door/lock-button (RRGBDL) 
    interface for a door controller using the Raspberry Pi serial port 
    and GPIO pins."""


    def __init__(self, 
                 port=PORT, 
                 baudrate=BAUD_RATE,
                 red = RED,
                 green = GREEN,
                 buzzer = BELL,
                 door = DOOR,
                 button = LOCK_BUTTON):

        #
        # Set up the hardware details for the controller interface.
        #
        self.SERIAL_PORT = port
        self.SERIAL_BPS = baudrate

        # Set the switches.
        self._red = switch.OnOff(red)
        self._green = switch.OnOff(green)
        self._door = switch.OnOff(door)
        self._button = switch.basic(button)
        self._buzzer = switch.OnOff(buzzer)

        self.serial_conn = serial.Serial(port, baudrate, timeout=0)

        if not self.serial_conn.isOpen():
            raise SerialConnectionError("Serial connection couldn't be open.")


    def poll_push_to_lock(self):
        """Check to see if the push-to-lock button has been pressed."""

        # The lock button has been pressed if the switch goes off.
        # ie: switch is "normally closed"
        return True if self._button.state == switch.OFF else False

    def poll_door_lock(self):
        """Check to see if the door is locked or not."""

        # If the door switch is on, the door is locked.
        # ie: switch is "normally open"
        return True if self._door.state == switch.ON else False


    def unlock(self):
        """Unlock the door."""
        self._door.flick(state=switch.OFF)

    def lock(self):
        """Lock the door"""
        self._door.flick(state=switch.ON)

    def toggle_red_led(self, on=None):
        """Toggle the red LED on, off or just toggle."""
        if on == None:
            self._red.flick()
        elif on:
            self._red.flick(state=switch.ON)
        else:
            self._red.flick(state=switch.OFF)

    def toggle_green_led(self, on=None):
        """Toggle the green LED on, off or just toggle."""
        if on == None:
            self._green.flick()
        elif on:
            self._green.flick(state=switch.ON)
        else:
            self._green.flick(state=switch.OFF)


    def buzz(self, freq=261, duration=1):
        """Buzz a piezo buzzer at a given frequency in Hz and a given
        duration in seconds.  The buzz frequency defaults to 261 Hz
        which is middle C on a piano."""
  
        # The period (in seconds) of a sound wave is the inverse of 
        # frequency in Hz.
        period = 1.0 / freq

        # Set the wait time to half of the period since we have to click
        # the buzzer on, then off.
        wait_time = period / 2

        # The number of waves to produce depends on the duration.
        total_cycles = int(freq * duration)

        for i in xrange(total_cycles):
            self._buzzer.flick(state=switch.ON)
            time.sleep(wait_time)
            self._buzzer.flick(state=switch.OFF)
            time.sleep(wait_time)


    def read_RFID(self, timeout=RFID_DEFAULT_TIMEOUT):
        """Read in an RFID card from the serial port and timeout after 
        the given number of seconds if we don't get any data."""

        self.lastRFID = None
        rfidCode = ""
        buildCode = False
        startTime = time.time()

        # Remove any garbage in the serial buffer and start from 
        # scratch.
        self.serial_conn.flushInput()


        ### READ LOOP ###
        while startTime + timeout > time.time():

            # Keep reading till we run out of bytes.
            while self.serial_conn.inWaiting() > 0: 

                rfidChr = self.serial_conn.read(1)
    
                # If we got a start byte, then start storing the code.
                if ord(rfidChr) == RFID_START_BYTE:
                    buildCode = True
                    rfidCode = ""
  
    
                # If we got a stop byte, then make sure we have enough
                # characters to build a code.  Otherwise, we have junk.
                elif ord(rfidChr) == RFID_STOP_BYTE:
                    if buildCode == True and \
                        len(rfidCode) == RFID_NUM_BYTES:

                        # We have a valid code!!!! Return it!!
                        # NOTE: any digits after 10 are checksum digits
                        #       so we strip them off.
                        self.lastRFID = rfidCode[0:10]
                        return self.lastRFID
   
                    buildCode = False
                    rfidCode = ""
  
  
                # We got a regular character so build the code. 
                elif buildCode:
  
                   # Check to make sure we still have a valid code. 
                   if len(rfidCode) < RFID_NUM_BYTES:
                       rfidCode += rfidChr
   
                   # The code is too long, we have garbage somewhere. 
                   else:
                       buildCode = False
                       rfidCode = ""
