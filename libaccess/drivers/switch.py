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

"""This is a module for abstracting the behaviour of plain-old every 
day switches which may or not be controllable via a Raspberry Pi."""


import RPi.GPIO as GPIO

### CONSTANTS ###
ON = 1
OFF = 0

# Set GPIO mode to Broadcom
GPIO.setmode(GPIO.BCM)

class basic():
    """Used for controlling push-button-type switches.  These ones, you
    can only check the status of the switch.  The Raspberry Pi can't set 
    the switch on or off, only the user can."""

    def __init__(self, pin):
        """Initialize an on/off switch.  By default, the starting state
        is off."""

        self._pin = pin
        self._state = OFF
 
        # Initialize the pin.
        self.reset()


    def reset(self):
        """Initialize the RPi GPIO pin to be in input mode.  Basic 
        switches are external manual switches and are read-only."""

        GPIO.cleanup(self._pin)
        GPIO.setup(self._pin, GPIO.IN)


    @property
    def state(self):
        """Returns the switch state.  If an RPi pin was specified
        on intialization, it reads the actual pin state."""

        if self._pin is not None:
            self._state = GPIO.input(self._pin)
        return ON if self._state else OFF



class OnOff(basic):
    """Used for switches that the RPi can control.  The user may set 
    them in real life, but we can change them also via code."""

    def reset(self):
        """Initialize the RPi GPIO pin to be in output mode.  On-Off 
        switches are controlled by the RPi itself."""

        GPIO.cleanup(self._pin)
        GPIO.setup(self._pin, GPIO.OUT)


    def flick(self, state=None):
        """Flick the switch on or off.  If an ON or OFF state is 
        specified explicitly, then set it accordingly."""

        # If no state is explicitly specified, set the pin to whatever
        # the opposite state is.  i.e., flick the switch  
        if state is None:
            if self.state == ON:
                GPIO.output(self._pin, GPIO.LOW)    
            elif self.state == OFF:
                GPIO.output(self._pin, GPIO.HIGH)

        # If a state was explicitly specified, set it. 
        elif state == ON:
            GPIO.output(self._pin, GPIO.HIGH)
        elif state == OFF:
            GPIO.output(self._pin, GPIO.LOW) 
