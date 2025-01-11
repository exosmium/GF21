import logging
import asyncio
import aiohttp
from telethon import TelegramClient, events, types, Button
from telethon.tl import functions, types as tl_types
from config import Config
from session_manager import SessionManager
from gps_service import GPSService
from vehicle_status import VehicleStatus
import lang

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GPSBot:
    """Main bot class handling Telegram interactions"""
    
    def __init__(self):
        self.config = Config()
        self.client = TelegramClient(
            'gps_bot_session',
            self.config.API_ID,
            self.config.API_HASH
        )
        self.session = None
        self.session_manager = None
        self.gps_service = None

    async def start(self):
        """Initialize and run the bot"""
        try:
            self.session = aiohttp.ClientSession()
            self.session_manager = SessionManager(self.config, self.session)
            self.gps_service = GPSService(self.config, self.session_manager, self.session)
            
            await self.session_manager.get_session()
            await self.setup_handlers()
            await self.client.start(bot_token=self.config.BOT_TOKEN)
            logger.info("Bot started successfully")
            await self.setup_bot_menu()
            await self.client.run_until_disconnected()
        finally:
            if self.session:
                await self.session.close()

    async def setup_bot_menu(self):
        """Set up the bot's command menu"""
        commands = [
            tl_types.BotCommand(command="start", description=lang.CMD_START),
            tl_types.BotCommand(command="help", description=lang.CMD_HELP)
        ]
        await self.client(functions.bots.SetBotCommandsRequest(
            commands=commands,
            scope=tl_types.BotCommandScopeDefault(),
            lang_code="ru"
        ))

    def get_keyboard(self):
        """Create inline keyboard with main buttons"""
        return [
            [
                Button.inline(lang.BUTTON_CHECK_STATUS, "check_status"),
                Button.inline(lang.BUTTON_UPDATE_LOCATION, "update_location")
            ]
        ]

    async def setup_handlers(self):
        """Set up command and callback handlers"""
        @self.client.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            await self.send_welcome_message(event)

        @self.client.on(events.NewMessage(pattern='/help'))
        async def help_handler(event):
            await self.send_help_message(event)

        @self.client.on(events.CallbackQuery)
        async def callback_handler(event):
            if event.data == b"check_status":
                await self.get_current_status(event)
            elif event.data == b"update_location":
                await self.request_location_update(event)

    def format_status_message(self, status: VehicleStatus) -> str:
        """Format the status message for Telegram"""
        return lang.STATUS_TEMPLATE.format(
            name=status.name,
            update_time=status.update_time.strftime('%d.%m.%Y %H:%M'),
            lat=status.lat,
            lng=status.lng,
            speed=status.speed,
            battery=status.battery
        )

    async def send_welcome_message(self, event):
        """Send welcome message with inline keyboard"""
        await event.respond(lang.WELCOME_MESSAGE, buttons=self.get_keyboard())

    async def send_help_message(self, event):
        """Send help message with command descriptions"""
        await event.respond(lang.HELP_MESSAGE, parse_mode='md', buttons=self.get_keyboard())

    async def request_location_update(self, event):
        """Handle location update request"""
        try:
            if hasattr(event, 'answer'):
                await event.answer()
            
            processing_msg = await event.respond(lang.PROCESSING_UPDATE)
            
            update_sent = await self.gps_service.request_location_update()
            
            if update_sent:
                await processing_msg.edit(
                    lang.UPDATE_SUCCESS,
                    buttons=self.get_keyboard()
                )
            else:
                await processing_msg.edit(
                    lang.UPDATE_FAILED,
                    buttons=self.get_keyboard()
                )

        except Exception as e:
            logger.error(f"Error in request_location_update: {str(e)}")
            await event.respond(
                lang.UPDATE_ERROR,
                buttons=self.get_keyboard()
            )

    async def get_current_status(self, event):
        """Handle current status request"""
        try:
            if hasattr(event, 'answer'):
                await event.answer()
            
            processing_msg = await event.respond(lang.GETTING_STATUS)
            
            data = await self.gps_service.fetch_device_data()
            if not data:
                await processing_msg.edit(
                    lang.STATUS_FAILED,
                    buttons=self.get_keyboard()
                )
                return

            status = VehicleStatus(data)
            message = self.format_status_message(status)
            
            await processing_msg.delete()
            
            # Send location message first
            await self.client.send_message(
                event.chat_id,
                file=types.InputMediaGeoPoint(
                    types.InputGeoPoint(
                        lat=status.lat,
                        long=status.lng
                    )
                )
            )
            
            # Send status message with keyboard
            await event.respond(
                message,
                parse_mode='md',
                buttons=self.get_keyboard()
            )

        except Exception as e:
            logger.error(f"Error in get_current_status: {str(e)}")
            await event.respond(
                lang.STATUS_ERROR,
                buttons=self.get_keyboard()
            )

async def main():
    """Entry point of the application"""
    bot = GPSBot()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())