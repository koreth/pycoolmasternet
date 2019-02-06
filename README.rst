pycoolmasternet
===============
A Python 3 library for interacting with a CoolMasterNet_ HVAC bridge.

.. _CoolMasterNet: https://coolautomation.com/products/coolmasternet/

Installation
------------
`pip install pycoolmasternet`

Or you can get the code from `https://github.com/koreth/pycoolmasternet`

Usage
-----

.. code-block:: python

    from pycoolmasternet import CoolMasterNet

    # Supply the IP address and optional port number (default 10102).
    #
    # By default, properties will be refreshed by querying the device
    # if last refresh was more than 1 second ago; pass auto_update=False
    # to disable that behavior (in which case you will need to call
    # update_status() explicitly).
    cool = CoolMasterNet('192.168.0.123', port=12345, auto_update=False)

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

    # Swing mode: horizontal, vertical, auto, 30, 45, 60, stop
    # Numeric settings are degrees of louver tilt. On read, the property can
    # be None if the bridge reports that the device doesn't support swing.
    device.swing
    device.set_swing('30')

    # Dict with all the properties listed above
    device.status

    # Force refresh of status (by default, device auto-updates its status
    # if most recent update is more than 1 second ago)
    device.update_status()

License
-------
This code is released under the MIT license.
