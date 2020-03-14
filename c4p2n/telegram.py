from ppm_telegram_bot_client.api_client import ApiClient, AsyncApis

from c4p2n.config import config

client = ApiClient(host=config.PPM_TELEGRAM_BOT_API_URL, timeout=120)

telegram_api = AsyncApis(client)
