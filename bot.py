import discord, os


TOKEN = os.environ["DISCORD_TOKEN"]

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):

        if message.author == client.user:
            return
        if message.content.startswith('!'):
            command = message.content[1:].split(" ")

            print(f'Message from {message.author}: {message.content}')
            await message.channel.send(f'{",".join(command)}')

client = MyClient()
client.run(TOKEN)

