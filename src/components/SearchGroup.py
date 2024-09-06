import asyncio
import configparser
from telethon import TelegramClient, functions, types

# Reading Configs
config = configparser.ConfigParser()
config.read("C:\\Users\\pande\\Downloads\\telegram-analysis-master\\telegram-analysis-master\\config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Initialize Telegram client
client = TelegramClient(username, api_id, api_hash)

# Define the keyword for filtering groups
keyword = 'ga'
group_list = []

async def main():
    await client.start()

    try:
        # Retrieve the dialogs (chats) in your account
        result = await client.get_dialogs()

        # Filter and print groups that match the keyword
        for dialog in result:
            if dialog.is_group or dialog.is_channel:
                if keyword.lower() in dialog.name.lower():
                    group_list.append(dialog.name)
        print(group_list)

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the client
if __name__ == "__main__":
    asyncio.run(main())
