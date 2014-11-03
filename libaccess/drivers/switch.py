# This is a module for abstracting the behaviour of plain-old every 
# day switches like light switches, but controlled by a pin on a 
# Raspberry Pi..

import RPi.GPIO as GPIO

### CONSTANTS ###
ON = 1
OFF = 0

class pushButton():
    """Used for controlling push-button-type switches.  These ones, you
    can only check the status of the button.  The Raspberry Pi can't set 
    the switch on or off."""


class onOffSwitch():
    """Used for manipulating any type of on/off switch.  E.g. a light
    switch."""

    def __init__(self, pin=None, state=OFF):
        """Initialize an on/off switch.  By default, the starting state
        is off."""

        self._pin = pin
        self._state = state
 
        if pin is not None:
            # initialize the pin and set the state accordingly.
            GPIO.setup(self._pin, GPIO.OUT)

    @property
    def state(self):
        """Returns the switch state.  If an RPi pin was specified
        on intialization, it reads the actual pin state."""

        if self._pin is not None:
            self._state = GPIO.input(self._pin)
        return ON if self._state else OFF


    def toggle(self, state=None):
        """Toggle the switch on or off.  If an ON or OFF state is 
        specified explicitly, then set it accordingly."""

        # If no state is explicitly specified, set the pin to whatever
        # the opposite state is.  i.e., duh, toggle it.
        if state is None:
            if self.state == ON:
                GPIO.output(self._pin, GPIO.LOW)    
            elif self.state = OFF:
                GPIO.output(self._pin, GPIO.HIGH)

        # If a state was explicitly specified, set it. 
        elif state == ON:
            GPIO.output(self._pin, GPIO.HIGH)
        elif state == OFF:
            GPIO.output(self._pin, GPIO.LOW) 
