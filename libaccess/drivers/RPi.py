#!/usr/bin/python
#
#        Copyright (C) 2014 Shawn Wilson
#        shawn@ch2a.ca
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


import RPi.GPIO as GPIO
import serial
import time


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
