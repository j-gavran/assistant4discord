from assistant4discord.assistant.commands.master.master_class import Master


class Ping(Master):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help = '```***Ping help***\n' \
                    'Ping discord server and return response time in ms.```'
        self.call = 'ping'

    async def doit(self):
        await self.message.channel.send('{} ms'.format(round(self.client.latency * 1000)))
