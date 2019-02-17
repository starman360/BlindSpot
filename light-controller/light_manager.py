#!/usr/bin/python
import time
import sys
import requests
from phue import Bridge

bridge_ip = '10.0.2.98'
webserver = 'http://127.0.0.1:8080/live'

b = Bridge(bridge_ip)

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)

# Get the bridge state (This returns the full dictionary that you can explore)

# Prints if light 1 is on or not
# b.get_light(1, 'on')
#
# # Set brightness of lamp 1 to max
# b.set_light(1, 'bri', 254)
#
# # Set brightness of lamp 2 to 50%
# b.set_light(2, 'bri', 127)
#
# # Turn lamp 2 on
# b.set_light(2,'on', True)
#
# # You can also control multiple lamps by sending a list as lamp_id
# b.set_light( [1,2], 'on', True)
#
# # Get the name of a lamp
# b.get_light(1, 'name')
#
# # You can also use light names instead of the id
# b.get_light('Kitchen')
# b.set_light('Kitchen', 'bri', 254)
#
# # Also works with lists
# b.set_light(['Bathroom', 'Garage'], 'on', False)
#
# # The set_light method can also take a dictionary as the second argument to do more fancy stuff
# # This will turn light 1 on with a transition time of 30 seconds
# command =  {'transitiontime' : 300, 'on' : True, 'bri' : 254}
# b.set_light(1, command)
#

old_light_data = {}
light_data = {}

def initphue():
    try:
        b.connect()
    except:
        print("Please press the button on the Philips Hue Bridge")
        sys.exit(-1)
    print("Connected Successfully to the Philips Hue Bridge!")

def getparkingdata():
    print("- Checking Parking Data")
    global light_data
    light_data = requests.get(webserver).json()

def setlighting():
    print("| Setting lighting")
    print(light_data)
    # if not (old_light_data == light_data):
    #     if
    #     light_data['A'][]

if __name__ == "__main__":
    initphue()
    while 1:
        getparkingdata()
        setlighting()
        time.sleep(10)
