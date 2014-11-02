# This is a module for abstracting the behaviour of plain-old every 
# day hardware interfaces have been used forever.  For example, switches, 
# knobs, buttons, etc.

### CONSTANTS ###
ON = 1
OFF = 0

class onOffSwitch():
    """Used for manipulating any type of on/off switch.  E.g. a light
    switch."""

    def __init__(self, state=OFF):
        """Initialize an on/off switch.  By default, the starting state
        is off."""

        self._state = state




