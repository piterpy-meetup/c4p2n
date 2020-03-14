from ppm_telegram_bot_client.api_client import ApiClient, AsyncApis

client = ApiClient(
    host="https://fb2e38d3-14e7-40f3-95d8-a3f4f44e69cc.api.beta.kintohub.com/ppm-telegram-bot-sl"
)

telegram_api = AsyncApis(client)
