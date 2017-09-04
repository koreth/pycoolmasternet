pycoolmasternet
=====
A Python 3 library for interacting with a
[CoolMasterNet](https://coolautomation.com/products/coolmasternet/) HVAC bridge.

Installation
------------
`pip install pycoolmasternet`

Or you can get the code from `https://github.com/koreth/pycoolmasternet`

Usage
-------
```python
import pycoolmasternet

# Supply the IP address and optional port number (default 10102).
cool = coolmasternet.CoolMasterNet('192.168.0.123', port=12345)

# Returns a list of CoolMasterDevice objects
devices = cool.devices()

# Device's unit ID on the CoolMasterNet bridge, e.g., "L7.001"
device.uid

# Temperature unit: imperial, celsius
device.unit

# Current reading of device's thermometer
device.temperature

# Current setting of device's thermostat
device.thermostat
device.set_thermostat(28)

# True if device is turned on
device.is_on
device.turn_on()
device.turn_off()

# Fan speed: low, med, high
device.fan_speed
device.set_fan_speed('med')

# Mode of operation: auto, cool, dry, fan, heat
device.mode
device.set_mode('cool')
```

License
-------
This code is released under the MIT license.
