# Copyright (C) 2013 Windsor Hackforge
#
# This module is part of RPi Door and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import RPi.GPIO as GPIO
import serial


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
                 baudrate=2400):
                 red = 24
                 green = 23
                 buzzer = 18
                 door = 25
                 button = 17)

        #
        # Set up the hardware details for the controller interface.
        #
        self.SERIAL_PORT = port
        self.SERIAL_BPS = baudrate
        self.RED = red
        self.GREEN = green
        self.BELL = buzzer
        self.DOOR = door
        self.BUTTON = button
      
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
        # pin 17 returns 1 when not pressed and 0 when pressed
        # ie: switch is "normally closed"
        return not GPIO.input(self.BUTTON)

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
  
        null


    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        """Check to see if the data to be set is greater than 41. If so,
        it sets itself to an empty bytearray.
        """
        if len(data) > 41:
            self._data = b""
        else:
            self._data = data
        return self._data


    def read_RFID(self, timeout=5):
        """Read in an RFID card from the serial port and timeout after 
        the given number of seconds if we don't get any data."""

        # flushes to remove any remaining bytes
        self.serial_conn.flushInput()
        self.data = b""

        # Read in all the data we have waiting on the serial buffer.
        while self.serial_conn.inWaiting() > 0:
            self.data += self.serial_conn.read(1)

        return str(self.data, 'utf-8')
