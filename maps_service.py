import time
import logging
import aiohttp
from typing import Optional
from config import Config
import lang

logger = logging.getLogger(__name__)

class MapsService:
    """Handles interactions with Google Maps services"""
    
    def __init__(self, config: Config, session: aiohttp.ClientSession):
        self.config = config
        self.session = session

    def _format_duration_in_russian(self, duration_text: str) -> str:
        """Convert English duration text to Russian format"""
        # Convert "X mins" or "X min" to Russian
        if "mins" in duration_text or "min" in duration_text:
            minutes = int(''.join(filter(str.isdigit, duration_text)))
            if minutes % 10 == 1 and minutes != 11:
                return f"{minutes} {lang.MINUTE_1}"
            elif 2 <= minutes % 10 <= 4 and (minutes < 10 or minutes > 20):
                return f"{minutes} {lang.MINUTE_2_4}"
            else:
                return f"{minutes} {lang.MINUTE_5_20}"
        
        # Convert "X hours Y mins" to Russian
        if "hours" in duration_text or "hour" in duration_text:
            parts = duration_text.split()
            hours = int(parts[0])
            minutes = int(parts[2]) if len(parts) > 2 else 0
            
            hours_text = ""
            if hours == 1:
                hours_text = f"1 {lang.HOUR_1}"
            elif 2 <= hours <= 4:
                hours_text = f"{hours} {lang.HOUR_2_4}"
            else:
                hours_text = f"{hours} {lang.HOUR_5_20}"
                
            if minutes == 0:
                return hours_text
            
            minutes_text = ""
            if minutes % 10 == 1 and minutes != 11:
                minutes_text = f"{minutes} {lang.MINUTE_1}"
            elif 2 <= minutes % 10 <= 4 and (minutes < 10 or minutes > 20):
                minutes_text = f"{minutes} {lang.MINUTE_2_4}"
            else:
                minutes_text = f"{minutes} {lang.MINUTE_5_20}"
                
            return f"{hours_text} {minutes_text}"
            
        return duration_text

    async def get_travel_time(self, origin_lat: float, origin_lng: float) -> str:
        """Get estimated travel time from current location to home"""
        try:
            timestamp = int(time.time() * 1000)
            url = (
                f"https://maps.googleapis.com/maps/api/directions/json"
                f"?origin={origin_lat},{origin_lng}"
                f"&destination={self.config.HOME_COORDS}"
                f"&mode=driving"
                f"&key={self.config.GOOGLE_MAPS_API_KEY}"
                f"&_={timestamp}"
            )
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'OK' and data.get('routes'):
                        duration_text = data['routes'][0]['legs'][0]['duration']['text']
                        return self._format_duration_in_russian(duration_text)
            return lang.STATUS_UNKNOWN
        except Exception as e:
            logger.error(f"Error getting travel time: {str(e)}")
            return lang.STATUS_UNKNOWN

    async def generate_map_image(self, lat: float, lng: float) -> Optional[bytes]:
        """Generate a static map image showing the route"""
        try:
            timestamp = int(time.time() * 1000)
            path_param = f"path=color:0x0000ff|weight:5|{lat},{lng}|{self.config.HOME_COORDS}"
            url = (
                f"https://maps.googleapis.com/maps/api/staticmap?size=600x400"
                f"&{path_param}"
                f"&markers=color:red%7Clabel:D%7C{lat},{lng}"
                f"&markers=color:blue%7Clabel:H%7C{self.config.HOME_COORDS}"
                f"&key={self.config.GOOGLE_MAPS_API_KEY}"
                f"&_={timestamp}"
            )
            headers = {
                "Accept": "image/jpeg, image/png, image/*",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    content_type = response.headers.get('Content-Type', '')
                    if 'image' in content_type:
                        return await response.read()
                    else:
                        logger.error(f"Unexpected content type: {content_type}")
                        return None
            return None
        except Exception as e:
            logger.error(f"Error generating map image: {str(e)}")
            return None