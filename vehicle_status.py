import re
import datetime
from typing import Tuple, Optional
from config import Config
import lang

class VehicleStatus:
    """Represents the current status of a vehicle"""
    
    def __init__(self, data: dict):
        info = data["customer_info_list"][0]
        self.name = info.get('name', 'Unknown')
        self.imei = info.get('imei', 'Unknown')
        self.update_time = self._parse_time(info.get('updatetime'))
        self.gps_time = self._parse_time(info.get('gpstime'))
        self.speed = self._parse_speed(info.get('speed', '0'))
        self.status = self._parse_status(info.get('online_status', ''))
        self.battery = int(info.get('bat', '0'))
        self.lat = float(info.get('lat_google', 0))
        self.lng = float(info.get('lng_google', 0))

    def _parse_time(self, time_str: str) -> datetime.datetime:
        """Parse time string into datetime object with correct timezone"""
        try:
            # Parse the server time (assumed to be in UTC)
            dt = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            utc_time = dt.replace(tzinfo=datetime.timezone.utc)
            
            # Convert to local timezone (Europe/Riga)
            local_time = utc_time.astimezone(Config.TIMEZONE)
            return local_time
        except (ValueError, TypeError):
            return Config.TIMEZONE.localize(datetime.datetime.now())

    def _parse_speed(self, speed: str) -> int:
        """Parse speed string into integer"""
        try:
            return int(float(speed))
        except (ValueError, TypeError):
            return 0

    def _parse_status(self, status: str) -> Tuple[str, Optional[int]]:
        """Parse status string into human-readable format"""
        if not status:
            return lang.STATUS_UNKNOWN, None
        
        match = re.match(r"Static(\d+)m", status)
        if match:
            minutes = int(match.group(1))
            return lang.STATUS_STATIC.format(minutes), minutes
            
        return status, None