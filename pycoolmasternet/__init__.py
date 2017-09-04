#!/usr/bin/env python3
import re
from telnetlib import Telnet
import time

__author__ = "Steven Grimm"
__copyright__ = "Copyright 2017 Steven Grimm"


class CoolMasterNet(object):
    def __init__(self, host, port=10102, read_timeout=1):
        """Initialize this CoolMasterNet instance to connect to a particular
        host at a particular port."""
        self._host = host
        self._port = port
        self._read_timeout = read_timeout

    def _make_request(self, request):
        """Send a request to the CoolMasterNet and returns the response."""
        # Can't use "with" because Python 2 telnetlib doesn't support it
        tn = Telnet(self._host, self._port)
        try:
            if tn.read_until(b">", self._read_timeout) != b">":
                raise Exception('CoolMasterNet prompt not found')
            
            request = request + "\n"
            tn.write(request.encode('ascii'))

            response = tn.read_until(b"\n>", self._read_timeout)
            response = response.decode('ascii')

            if response.endswith("\n>"):
                response = response[:-1]

            if response.endswith("OK\r\n"):
                response = response[:-4]

            return response
        finally:
            tn.close()

    def devices(self):
        """Return a list of CoolMasterNetDevice objects representing the
        devices attached to the bridge."""
        status_lines = self._make_request("ls").strip().split("\r\n")
        return [CoolMasterNetDevice(self, line[0:6]) for line in status_lines]


class CoolMasterNetDevice(object):
    """A device attached to a CoolMasterNet bridge.

    This object caches data for 1 second so that reading a bunch of its
    properties in rapid succession doesn't require repeated server
    requests."""

    def __init__(self, bridge, uid):
        """Initializes a new device given its unit identifier."""
        self._bridge = bridge
        self._uid = uid
        self._last_refresh_time = 0

    def _update_status(self):
        """Fetches the device's current status from the bridge if needed."""
        if time.time() - self._last_refresh_time < 1:
            return

        status_line = self._bridge._make_request('ls2 ' + self._uid)

        # Status line looks like
        # L7.001 ON  073.0F 077.7F Low  Cool OK   - 0
        fields = re.split(r"\s+", status_line.strip())
        if len(fields) != 9:
            raise Exception('Unexpected status line format: ' + str(fields))

        self._is_on = fields[1] == 'ON'
        self._unit = 'imperial' if fields[2][-1] == 'F' else 'celsius'
        self._thermostat = float(fields[2][:-1])
        self._temperature = float(fields[3][:-1])
        self._fan_speed = fields[4].lower()
        self._mode = fields[5].lower()

        self._last_refresh_time = time.time()

    def _clear_status(self):
        """Forces the next property read to refresh the device status."""
        self._last_refresh_time = 0

    def _make_request(self, format_str):
        """Makes a request to the bridge. Replaces {} in format_str with
        device's unit ID."""
        return self._bridge._make_request(format_str.format(self._uid))

    def set_fan_speed(self, value):
        self._make_request('fspeed {} ' + value)
        self._clear_status()

    def set_mode(self, value):
        self._make_request(value + ' {}')
        self._clear_status()

    def set_thermostat(self, value):
        self._make_request('temp {}')
        self._clear_status()

    def turn_on(self):
        """Turns the device on."""
        self._make_request('on {}')
        self._clear_status()

    def turn_off(self):
        """Turns the device off."""
        self._make_request('off {}')
        self._clear_status()

    def update_status(self):
        """Forces a status update. Normally, status is queried automatically
        if it hasn't been updated in the past second."""
        self._clear_status()
        self._update_status()

    @property
    def fan_speed(self):
        self._update_status()
        return self._fan_speed

    @property
    def is_on(self):
        self._update_status()
        return self._is_on

    @property
    def mode(self):
        self._update_status()
        return self._mode

    @property
    def status(self):
        self._update_status()
        return {
            'fan_speed': self._fan_speed,
            'is_on': self._is_on,
            'mode': self._mode,
            'temperature': self._temperature,
            'thermostat': self._thermostat,
            'uid': self._uid,
            'unit': self._unit
        }

    @property
    def temperature(self):
        self._update_status()
        return self._temperature

    @property
    def thermostat(self):
        self._update_status()
        return self._thermostat

    @property
    def uid(self):
        return self._uid

    @property
    def unit(self):
        self._update_status()
        return self._unit
