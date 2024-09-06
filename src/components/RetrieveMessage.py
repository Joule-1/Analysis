def message_retrieval():

    import configparser
    import json
    from datetime import datetime
    from telethon import TelegramClient, events
    from telethon.errors import SessionPasswordNeededError
    from telethon.tl.functions.messages import GetHistoryRequest
    from telethon.tl.types import PeerChannel

    # Custom JSON encoder for datetime and bytes
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return super().default(o)

    # Reading Configs
    config = configparser.ConfigParser()
    config.read("telegram-analysis\\src\\config\\config.ini")

    # Setting configuration values
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    phone = config['Telegram']['phone']
    username = config['Telegram']['username']

    # Create the client and connect
    client = TelegramClient(username, api_id, api_hash)

    async def fetch_and_save_history(client, channel, filename):
        offset_id = 0
        limit = 100
        all_messages = []

        while True:
            try:
                print("Fetching messages from offset ID:", offset_id)
                history = await client(GetHistoryRequest(
                    peer=channel,
                    offset_id=offset_id,
                    limit=limit,
                    max_id=0,
                    min_id=0,
                    hash=0,
                    add_offset=0,
                    offset_date=None
                ))
                
                if not history.messages:
                    break
                
                messages = history.messages
                for message in messages:
                    message_data = {
                        'id': message.id,
                        'date': message.date,
                        'text': message.message,
                    }
                    all_messages.append(message_data)
                
                offset_id = messages[-1].id
                print("Fetched", len(messages), "messages")
            
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    # telegram-analysis\src\data\Testing.json
        try:
            with open(f"telegram-analysis\\src\\data\\{filename}", 'w') as outfile:
                json.dump(all_messages, outfile, cls=DateTimeEncoder)
        except IOError as e:
            print(f'Failed to write historical messages to file: {e}')

        # Setup event listener for new messages
        @client.on(events.NewMessage)
        async def handler(event):
            await handle_new_messages(event, filename)
        
        print("Client is running. Waiting for new messages...")
        await client.run_until_disconnected()

    async def handle_new_messages(event, filename):
        # Prepare message data
        message_data = {
            'id': event.message.id,
            'date': event.message.date,
            'text': event.message.text,
        }

        # Read existing messages
        try:
            with open(f"telegram-analysis\\src\\data\\{filename}", 'r') as outfile:
                all_messages = json.load(outfile)
        except (IOError, json.JSONDecodeError):
            all_messages = []

        # Prepend new message to the list
        all_messages.insert(0, message_data)

        # Write updated list of messages back to the file
        try:
            with open(f"telegram-analysis\\src\\data\\{filename}", 'w') as outfile:
                json.dump(all_messages, outfile, cls=DateTimeEncoder)
        except IOError as e:
            print(f'Failed to write new message to file: {e}')

    async def main(phone):
        await client.start()
        print("Client Created")
        
        # Ensure you're authorized
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=input('Password: '))

        user_input_channel = input('Enter entity (Telegram URL or entity ID):')
        if user_input_channel.isdigit():
            entity = PeerChannel(int(user_input_channel))
        else:
            entity = user_input_channel

        my_channel = await client.get_entity(entity)
        
        # Fetch and save historical messages
        filename = my_channel.title + ".json" or f"Chat_{my_channel.id}.json"
        await fetch_and_save_history(client, my_channel, filename)

    with client:
        client.loop.run_until_complete(main(phone))

message_retrieval()