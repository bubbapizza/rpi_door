# Initialize the RPi pins as soon as this driver is imported.

import RPi.GPIO as GPIO

# Set pin mode to Broadcom.
GPIO.setmode(GPIO.BCM)
