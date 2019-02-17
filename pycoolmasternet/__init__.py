#!/usr/bin/env python3
import re
from telnetlib import Telnet
import time

__author__ = "Steven Grimm"
__copyright__ = "Copyright 2019 Steven Grimm"


_SWING_CHAR_TO_NAME = {
    "-": None,
    "0": None,
    "a": "auto",
    "h": "horizontal",
    "3": "30",
    "4": "45",
    "6": "60",
    "v": "vertical",
    "x": "stop",
}

_SWING_NAME_TO_CHAR = {
    "auto": "a",
    "horizontal": "h",
    "30": "3",
    "45": "4",
    "60": "6",
    "vertical": "v",
    "stop": "x",
}

_FAN_SPEEDS = ["low", "med", "high"]
_MODES = ["auto", "cool", "dry", "fan", "heat"]


def autoupdate_property(func):
    def update_and_get(*args):
        args[0]._update_if_needed()
        return func(*args)

    return property(update_and_get)


class CoolMasterNet(object):
    def __init__(self, host, port=10102, read_timeout=1, auto_update=True):
        """Initialize this CoolMasterNet instance to connect to a particular
        host at a particular port."""
        self._host = host
        self._port = port
        self._read_timeout = read_timeout
        self._auto_update = auto_update

    def _make_request(self, request):
        """Send a request to the CoolMasterNet and returns the response."""
        # Can't use "with" because Python 2 telnetlib doesn't support it
        tn = Telnet(self._host, self._port)
        try:
            if tn.read_until(b">", self._read_timeout) != b">":
                raise Exception("CoolMasterNet prompt not found")

            request = request + "\n"
            tn.write(request.encode("ascii"))

            response = tn.read_until(b"\n>", self._read_timeout)
            response = response.decode("ascii")

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
        return [
            CoolMasterNetDevice(self, line[0:6], self._auto_update)
            for line in status_lines
        ]


class CoolMasterNetDevice(object):
    """A device attached to a CoolMasterNet bridge.

    This object caches data for 1 second so that reading a bunch of its
    properties in rapid succession doesn't require repeated server
    requests."""

    def __init__(self, bridge, uid, auto_update=True):
        """Initialize a new device given its unit identifier."""
        self._bridge = bridge
        self._uid = uid
        self._last_refresh_time = 0
        self._auto_update = auto_update

    def _update_if_needed(self):
        """Check whether the existing status is too stale and update it if so."""
        if self._auto_update and time.time() - self._last_refresh_time >= 1:
            self._update_status()

    def _update_status(self):
        """Fetch the device's current status from the bridge."""
        status_line = self._bridge._make_request("ls2 " + self._uid)

        # Status line looks like
        # L7.001 ON  073.0F 077.7F Low  Cool OK   - 0
        fields = re.split(r"\s+", status_line.strip())
        if len(fields) != 9:
            raise Exception("Unexpected status line format: " + str(fields))

        self._is_on = fields[1] == "ON"
        self._unit = "imperial" if fields[2][-1] == "F" else "celsius"
        self._thermostat = float(fields[2][:-1])
        self._temperature = float(fields[3][:-1])
        self._fan_speed = fields[4].lower()
        self._mode = fields[5].lower()

        swing_line = self._bridge._make_request("query {} s".format(self._uid))
        self._swing_mode = _SWING_CHAR_TO_NAME[swing_line.strip()]

        self._last_refresh_time = time.time()

    def _clear_status(self):
        """Force the next property read to refresh the device status if
        autoupdate mode is active."""
        self._last_refresh_time = 0

    def _make_request(self, format_str):
        """Make a request to the bridge. "UID" in format_str is replaced with
        device's unit ID."""
        return self._bridge._make_request(format_str.replace("UID", self._uid))

    def set_fan_speed(self, value):
        self._make_request("fspeed UID {}".format(value))
        self._clear_status()

    def set_mode(self, value):
        if value in _MODES:
            self._make_request(value + " UID")
            self._clear_status()
        else:
            raise ValueError(
                "Unrecognized mode {}. Valid values: {}".format(value, " ".join(_MODES))
            )

    def set_thermostat(self, value):
        self._make_request("temp UID {}".format(value))
        self._clear_status()

    def set_swing(self, value):
        if value in _SWING_NAME_TO_CHAR:
            self._make_request("swing UID {}".format(_SWING_NAME_TO_CHAR[value]))
            self._clear_status()
        else:
            raise ValueError(
                "Unrecognized swing mode {}. Valid values: {}".format(
                    value, " ".join(_SWING_NAME_TO_CHAR.keys())
                )
            )

    def turn_on(self):
        """Turn the device on."""
        self._make_request("on UID")
        self._clear_status()

    def turn_off(self):
        """Turn the device off."""
        self._make_request("off UID")
        self._clear_status()

    def update_status(self):
        """Force a status update. Normally, status is queried automatically
        if it hasn't been updated in the past second."""
        self._clear_status()
        self._update_status()

    @autoupdate_property
    def fan_speed(self):
        return self._fan_speed

    @autoupdate_property
    def is_on(self):
        return self._is_on

    @autoupdate_property
    def mode(self):
        return self._mode

    @autoupdate_property
    def status(self):
        return {
            "fan_speed": self._fan_speed,
            "is_on": self._is_on,
            "mode": self._mode,
            "swing": self._swing_mode,
            "temperature": self._temperature,
            "thermostat": self._thermostat,
            "uid": self._uid,
            "unit": self._unit,
        }

    @autoupdate_property
    def swing(self):
        return self._swing_mode

    @autoupdate_property
    def temperature(self):
        return self._temperature

    @autoupdate_property
    def thermostat(self):
        return self._thermostat

    @property
    def uid(self):
        return self._uid

    @autoupdate_property
    def unit(self):
        return self._unit
