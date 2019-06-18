from assistant4discord.nlp_tasks.message_processing import word2vec_input
from assistant4discord.assistant.commands.master.master_class import Master


class Help(Master):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.call = 'help'
        self.help = 'srsly?'

    async def doit(self):

        message = self.message.content[22:]

        if len(word2vec_input(message)) > 1:
            for i, (command_str, command) in enumerate(self.commands.items()):
                if command_str.lower() in message.lower():
                    await self.message.channel.send(command.help)
                    break

                if i == len(self.commands) - 1:
                    await self.message.channel.send('Command not found!')

        else:
            command_str = 'My commands: '
            for i, command_str_ in enumerate(self.commands.keys()):
                if i < len(self.commands) - 1:
                    command_str += command_str_ + ', '
                else:
                    command_str += command_str_

            command_str += '\nType help <command> for more info!'

            await self.message.channel.send(command_str)
