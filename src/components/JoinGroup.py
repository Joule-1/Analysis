import asyncio
import configparser
from telethon import TelegramClient, functions, types
from telethon.tl.functions.channels import JoinChannelRequest

# Reading Configs
config = configparser.ConfigParser()
config.read("telegram-analysis\\src\\config\\config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the Telegram client
client = TelegramClient(username, api_id, api_hash)

async def main():
    # Start the client
    await client.start(phone)
    
    # Join a group
    group_username = 'StriverStroy'  # Replace with actual group username or invite link
    try:
        await client(JoinChannelRequest(group_username))
        print(f'Successfully joined the group: {group_username}')
    except Exception as e:
        print(f'An error occurred: {e}')

# Run the client
if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
