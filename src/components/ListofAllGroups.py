def group_list():
    import asyncio
    import configparser
    from telethon import TelegramClient, functions, types

    config = configparser.ConfigParser()
    config.read("telegram-analysis\\src\\config\\config.ini")

    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    username = config['Telegram']['username']

    client = TelegramClient(username, api_id, api_hash)

    async def main():
        await client.start()

        group_list_data = []

        try:
            result = await client.get_dialogs()

            for dialog in result:
                if dialog.is_group or dialog.is_channel:
                    group_list_data.append({'name': dialog.name})
                    # print(f"Chat ID: {dialog.id}, Title: {dialog.name}")

        except Exception as e:
            return {'error' : str(e)}
            # print(f"An error occurred: {e}")

        return group_list_data

    return asyncio.run(main())
    