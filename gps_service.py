import json
import time
import logging
import aiohttp
from typing import Optional, Dict
from session_manager import SessionManager
from vehicle_status import VehicleStatus
from config import Config

logger = logging.getLogger(__name__)

class GPSService:
    """Handles communication with the GPS tracking service"""
    
    def __init__(self, config: Config, session_manager: SessionManager, session: aiohttp.ClientSession):
        self.config = config
        self.session_manager = session_manager
        self.session = session

    async def request_location_update(self) -> bool:
        """Request device to update its location"""
        try:
            phpsessid = await self.session_manager.get_session()
            url = f"{self.config.BASE_URL}/post_submit_sendloc.php"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": f"PHPSESSID={phpsessid}",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.9",
                "Origin": self.config.BASE_URL,
                "Referer": f"{self.config.BASE_URL}/map.php"
            }
            
            async with self.session.post(
                url,
                headers=headers,
                data={"imei": self.config.IMEI},
                ssl=False
            ) as response:
                if response.status == 200:
                    text = await response.text()
                    logger.info(f"Location update response: {text}")
                    return "1" in text or "Y" in text
                return False
        except Exception as e:
            logger.error(f"Error requesting location update: {str(e)}")
            return False

    async def fetch_device_data(self) -> Optional[Dict]:
        """Fetch current device data from the GPS service"""
        try:
            phpsessid = await self.session_manager.get_session()
            timestamp = int(time.time() * 1000)
            url = f"{self.config.BASE_URL}/post_device_table_list.php?_nocache={timestamp}"
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": f"PHPSESSID={phpsessid}",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.9",
                "Origin": self.config.BASE_URL,
                "Referer": f"{self.config.BASE_URL}/map.php"
            }

            async with self.session.post(
                url,
                headers=headers,
                data={
                    "imei": self.config.IMEI,
                    "_": timestamp
                },
                ssl=False
            ) as response:
                if response.status == 200:
                    text = await response.text('utf-8-sig')
                    try:
                        start = text.find('{"customer_info_list":[{')
                        if start == -1:
                            logger.error("Could not find customer_info_list in response")
                            return None
                            
                        end = text.find('}],"aaData":[')
                        if end == -1:
                            logger.error("Could not find proper end of JSON object")
                            return None
                            
                        clean_json = text[start:end + 2] + "}"
                        return json.loads(clean_json)
                    except json.JSONDecodeError as json_err:
                        logger.error(f"JSON parsing error: {str(json_err)}")
                        return None
                        
                logger.error(f"HTTP Status: {response.status}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching device data: {str(e)}")
            return None