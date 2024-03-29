from bs4 import BeautifulSoup
from datetime import timedelta,datetime
import requests, json, sys

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity, generate_entity_id

from homeassistant.components.sensor import PLATFORM_SCHEMA, ENTITY_ID_FORMAT
from homeassistant.const import (CONF_NAME)

_LOGGER = logging.getLogger(__name__)
DEFAULT_NAME       = 'Skolmaten'
CONF_NAME          = 'name'
CONF_SENSORS       = 'sensors'
CONF_OFFSET        = 'offset'
CONF_LIMIT         = 'limit'
CONF_TYPE          = 'type'
SENSOR_OPTIONS = {
    'school': ('Skola')
}

SCAN_INTERVAL = timedelta(hours=4)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_TYPE, default='weeks'): vol.In(["days", "weeks"]),
    vol.Optional(CONF_OFFSET, default=0): vol.All(vol.Coerce(int), vol.Range(min=-10, max=10)),
    vol.Optional(CONF_LIMIT, default=1): cv.positive_int,
    vol.Required(CONF_SENSORS, default=[]): vol.Optional(cv.ensure_list, [vol.In(SENSOR_OPTIONS)]),
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Skolmaten sensor."""
    sensor_name = config.get(CONF_NAME)
    sensors     = config.get(CONF_SENSORS)
    type        = config.get(CONF_TYPE)
    offset      = config.get(CONF_OFFSET)
    limit       = config.get(CONF_LIMIT)
    devices     = []

    for sensor in sensors:
        devices.append(SkolmatenSensor(sensor_name, sensor['school'], sensor, type, offset, limit, hass))
    add_devices(devices, True)

# pylint: disable=no-member
class SkolmatenSensor(Entity):
    """Representation of a Skolmaten sensor."""
    page = ""

    def __init__(self, sensor_name, name, sensor, type, offset, limit, hass, day=0):
        """Initialize a Skolmaten sensor."""
        self._item       = sensor
        self._school     = sensor['school']
        self.offset      = offset
        self.limit       = limit
        self.type        = type
        self._name       = "{} {}".format(sensor_name, name)
        self._entity_id  = generate_entity_id(ENTITY_ID_FORMAT, self._name, hass=hass)
        self._attributes = None
        self._result     = None

    @property
    def entity_id(self):
        """Return the name of the sensor."""
        return self._entity_id

    @property
    def friendly_name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        if self._state is not None:
            return self._state
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the monitored installation."""
        if self._attributes is not None:
            return self._attributes

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ""

    @property
    def icon(self):
        """ Return the icon for the frontend."""
        return 'mdi:food'

    def update(self):
        #update values
        url = 'https://skolmaten.se/%s/rss/%s/?offset=%d&limit=%d' % (self._school, self.type, self.offset, self.limit)
        SkolmatenSensor.page = requests.get(url)
        self._result         = BeautifulSoup(SkolmatenSensor.page.content, "html.parser")
        self._attributes     = {}
        school = []
        for item in self._result.select('item'):
            day        = item.select('title')[0].text.strip()
            food       = item.select('description')[0].text.strip()
            date       = item.select('pubDate')[0].text
            parsedDate = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
            if "todaysFood" not in vars():
                todaysFood = "no food found for today"

            if parsedDate.date() == datetime.today().date():
                todaysFood = food

            school.append({
                'day' : day,
                'date': date,
                'food': food
            });
        self._state = sys.getsizeof(school)
        if "todaysFood" in vars():
            self._attributes.update({"todaysFood": todaysFood})
        self._attributes.update({"entries": school})
