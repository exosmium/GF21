import configparser
import pytz
from dataclasses import dataclass

def load_config(file_path='config.txt'):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

@dataclass
class Config:
    """Configuration settings for the GPS Bot"""
    _config = load_config()
    
    # Telegram settings
    API_ID: str = _config['Telegram']['API_ID']
    API_HASH: str = _config['Telegram']['API_HASH']
    BOT_TOKEN: str = _config['Telegram']['BOT_TOKEN']
    
    # GPS settings
    BASE_URL: str = _config['GPS']['BASE_URL']
    IMEI: str = _config['GPS']['IMEI']
    PASSWORD: str = _config['GPS']['PASSWORD']
    
    # Maps settings
    GOOGLE_MAPS_API_KEY: str = _config['Maps']['GOOGLE_MAPS_API_KEY']
    HOME_COORDS: str = _config['Maps']['HOME_COORDS']
    
    # App settings
    TIMEZONE = pytz.timezone(_config['App']['TIMEZONE'])
    UPDATE_RETRY_COUNT: int = int(_config['App']['UPDATE_RETRY_COUNT'])
    UPDATE_RETRY_DELAY: float = float(_config['App']['UPDATE_RETRY_DELAY'])
    SESSION_REFRESH_INTERVAL: int = int(_config['App']['SESSION_REFRESH_INTERVAL'])