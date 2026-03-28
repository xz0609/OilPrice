"""
A component which allows you to parse http://www.qiyoujiage.com/zhejiang.shtml get oil price

For more details about this component, please refer to the documentation at
https://github.com/SeanChengN/OilPrice/

"""
import re
import logging
import voluptuous as vol
import datetime
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)
from homeassistant.const import (CONF_NAME, CONF_REGION)
from requests import request, exceptions
from bs4 import BeautifulSoup

__version__ = '1.0.1'
_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['requests', 'beautifulsoup4']

COMPONENT_REPO = 'https://github.com/xz0609/OilPrice/'
SCAN_INTERVAL = datetime.timedelta(hours=8)
ICON = 'mdi:gas-station'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_REGION): cv.string,
})

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up oil price sensor from a config entry."""
    _LOGGER.info("Setting up oil price sensor from config entry")
    
    # 从配置条目获取配置
    config = config_entry.data
    name = config.get(CONF_NAME)
    region = config.get(CONF_REGION)
    
    # 创建传感器
    sensor = OilPriceSensor(name=name, region=region)
    
    # 添加到HA
    async_add_entities([sensor], True)
    
    return True

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up oil price sensor from YAML configuration."""
    _LOGGER.info("Setting up oil price sensor from YAML")
    async_add_entities([OilPriceSensor(name=config[CONF_NAME], region=config[CONF_REGION])], True)

class OilPriceSensor(Entity):
    def __init__(self, name: str, region: str):
        self._name = name
        self._region = region
        self._state = None
        self._entries = {}
        self._available = True

    def update(self):
        """Update sensor data."""
        _LOGGER.info("Updating oil price info from http://www.qiyoujiage.com/")
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
            }
            response = request('GET', 'http://m.qiyoujiage.com/' + self._region + '.shtml', 
                              headers=header, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, "lxml")
            dls = soup.select('#content > div.table_wrap > div.content_youjia > dl')
            _state = soup.select('#content > div.table_wrap > div.tishi')[0].text.strip()
            if '\n' in _state:
                self._state = _state.split('\n')[1]
            
            for dl in dls:
                match = re.search(r"\d+", dl.select('dt')[0].text)
                if match:
                    k = match.group()
                    price = dl.select('dd')[0].text
                    if "元" in price:
                        self._entries[k] = price.replace("(", "").replace("元", "").replace(")", "") #去除中文字符"元"，方便自动化直接使用数字
                    else:
                        self._entries[k] = price
            self._entries["update_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._entries["tips"] = soup.select('#content > div.table_wrap > div.tishi > span:nth-child(1)')[0].text.strip()
            self._entries["status"] = "online"
            self._available = True
            
        except Exception as err:
            _LOGGER.error("Error updating oil price data: %s", err)
            self._state = "Unavailable"
            self._entries["status"] = "offline"
            self._entries["error"] = str(err)
            self._entries["update_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._available = False

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return ICON

    @property
    def available(self):
        """Return if entity is available."""
        return self._available

    @property
    def extra_state_attributes(self):
        return self._entries

    @property
    def should_poll(self):
        """Return True if the sensor should be polled."""
        return True
