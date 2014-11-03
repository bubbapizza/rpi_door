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
to do with anything and is just an arbitrary API that I made up."""


import serial
import time
import RPi.GPIO as GPIO
import switch

#### CONSTANTS ####

# These values are specifically for the Parallax 28140 serial
# RFID reader as described at http://www.parallax.com/product/28140
RFID_NUM_BYTES = 10
RFID_START_BYTE = 10
RFID_STOP_BYTE = 13


class SerialConnectionError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class rrgbdl():
    """ This is an rfid/red/green/buzzer/door/lock (RRGBDL) interface for 
    a door controller using the Raspberry Pi serial port and GPIO pins."""


    def __init__(self, 
                 port="/dev/ttyAMA0", 
                 baudrate=2400,
                 red = 24,
                 green = 23,
                 buzzer = 18,
                 door = 25,
                 button = 17):

        #
        # Set up the hardware details for the controller interface.
        #
        self.SERIAL_PORT = port
        self.SERIAL_BPS = baudrate
        self.BELL = buzzer

        # Set the switches.
        self.red = switch.OnOff(red)
        self.green = switch.OnOff(green)
        self.door = switch.OnOff(door)
        self.button = switch.basic(button)

      
        #
        # Initialize the hardware.
        #
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.GREEN, GPIO.OUT)
        GPIO.setup(self.RED, GPIO.OUT)
        GPIO.setup(self.DOOR, GPIO.OUT)
        GPIO.setup(self.BELL, GPIO.OUT)
        GPIO.setup(self.BUTTON, GPIO.IN)

        self.serial_conn = serial.Serial(port, baudrate, timeout=0)

        if not self.serial_conn.isOpen():
            raise SerialConnectionError("Serial connection couldn't be open.")


    def poll_push_to_lock(self):
        # The lock button returns 1 when not pressed and 0 when pressed
        # ie: switch is "normally closed"
        return True if not GPIO.input(self.BUTTON) else False

    def poll_door_lock(self):
        """Check to see if the door is locked or not.  Return True or 
        False"""
        return True if GPIO.input(self.DOOR) else False


    def unlock(self):
        GPIO.output(self.DOOR, GPIO.LOW)

    def lock(self):
        GPIO.output(self.DOOR, GPIO.HIGH)


    def toggle_red_led(self, on=False):
        if on:
            GPIO.output(self.RED, GPIO.HIGH)
        else:
            GPIO.output(self.RED, GPIO.LOW)

    def toggle_green_led(self, on=False):
        if on:
            GPIO.output(self.GREEN, GPIO.HIGH)
        else:
            GPIO.output(self.GREEN, GPIO.LOW)


    def buzz(self, freq=3000, duration=1):
        """Buzz a piezo buzzer at a given frequency in Hz and a given
        duration in seconds."""
  
        # The period (in seconds) of a sound wave is the inverse of 
        # frequency in Hz.
        period = 1.0 / freq

        # Set the wait time to half of the period since we have to click
        # the buzzer on, then off.
        wait_time = period / 2

        # The number of waves to produce depends on the duration.
        total_cycles = freq * duration

        for i in xrange(total_cycles):
            GPIO.output(self.BELL, GPIO.HIGH)
            time.sleep(wait_time)
            GPIO.OUTPUT(self.BELL, GPIO.LOW)
            time.sleep(wait_time)


    def read_RFID(self, timeout=5):
        """Read in an RFID card from the serial port and timeout after 
        the given number of seconds if we don't get any data."""

        self.lastRFID = None
        rfidCode = ""
        startTime = time.time()

        while startTime + timeout > time.time():
   
            # Keep reading till we run out of bytes or we hit the
            # timeout period. 
            while self.serial_conn.inWaiting() > 0 and
                    startTime + timeout <= time.time():
    
                rfidChr = self.serial_conn.read(1)
    
                # If we got a start byte, then start storing the code.
                if ord(rfidChr) == RFID_START_BYTE:
                    buildCode = True
                    rfidCode = ""
  
    
                # If we got a stop byte, then make sure we have enough
                # characters to build a code.  Otherwise, we have junk.
                elif ord(rfidChr) == RFID_STOP_BYTE:
                    if buildCode == True and 
                            len(rfidCode) == RFID_NUM_BYTES:
                        self.lastRFID = rfidCode
   
                    buildCode = False
                    rfidCode = ""
  
  
                # We got a regular character so build the code. 
                elif buildCode:
  
                   # Check to make sure we still have a valid code. 
                   if len(rfidCode) < RFID_NUM_BYTES:
                       rfidCode += rfidChr
   
                   # The code is too long, we have garbage somewhere. 
                   else
                       buildCode = False
                       rfidCode = ""

        if self.lastRFID != None:
           return self.lastRFID 
