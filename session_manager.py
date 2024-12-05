import time
import logging
import aiohttp
from config import Config

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages the HTTP session and authentication with the GPS service"""
    
    def __init__(self, config: Config, session: aiohttp.ClientSession):
        self.config = config
        self.session = session
        self.phpsessid = None
        self.last_refresh = 0

    async def get_session(self) -> str:
        """Get a valid session ID, refreshing if necessary"""
        current_time = time.time()
        if not self.phpsessid or (current_time - self.last_refresh) > self.config.SESSION_REFRESH_INTERVAL:
            await self.refresh_session()
        return self.phpsessid

    async def refresh_session(self):
        """Refresh the session by authenticating with the GPS service"""
        try:
            url = f"{self.config.BASE_URL}/npost_login.php"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36",
                "Accept": "text/plain, */*; q=0.01",
                "Origin": self.config.BASE_URL,
                "Referer": f"{self.config.BASE_URL}/login.php"
            }
            data = {
                "demo": "F",
                "username": self.config.IMEI,
                "password": self.config.PASSWORD,
                "save_pwd": "1",
                "form_type": "0"
            }
            
            async with self.session.post(url, headers=headers, data=data, ssl=False) as response:
                if response.status == 200:
                    cookies = response.cookies
                    self.phpsessid = cookies.get('PHPSESSID').value
                    self.last_refresh = time.time()
                    logger.info("Successfully refreshed session")
                else:
                    logger.error(f"Failed to refresh session. Status: {response.status}")
        except Exception as e:
            logger.error(f"Error refreshing session: {str(e)}")