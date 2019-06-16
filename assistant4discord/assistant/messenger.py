from assistant4discord.nlp_tasks.similarity import Similarity
from importlib import import_module
import os
import inspect
import numpy as np


class Commander:

    def __init__(self, client, model_name, dir_path=None):
        """Commands initializer.

        Args:
            client: discord client from MyClient
            model_name: w2v model
            dir_path: if commands not in assistant4discord.assistant.commands

            self.commands: dict of commands from commands dir, {'command': command obj, ...}
            self.calls: list of command calls from commands, ['command call', ...]
            self.sim: w2v model class
            self.command_vectors: pre calculate command text sentence vectors from self.calls
        """
        self.client = client
        self.commands = self.get_commands(dir_path)
        self.calls = self.get_command_calls()
        self.set_help_command()

        self.sim = Similarity(model_name)
        self.command_vectors = self.sim.get_sentence2vec(self.calls)

    @staticmethod
    def get_commands(dir_path) -> dict:
        command_dct = {}

        if not dir_path:
            dir_path = os.path.dirname(os.path.realpath(__file__)) + '/commands'

        file_lst = os.listdir(dir_path)

        for file in file_lst:
            if file.endswith('.py') and '__init__' not in file:
                module = import_module('assistant4discord.assistant.commands.{}'.format(file[:-3]))
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and name != 'Master':
                        print('imported command: {}'.format(name))
                        command_dct['{}'.format(name).lower()] = obj()

        return command_dct

    def get_command_calls(self):
        command_calls = []

        for command_str, command in self.commands.items():
            command_calls.append(command.call)

        return command_calls

    def set_help_command(self):
        self.commands['help'].commands = self.commands


class Messenger(Commander):
    """Class for interacting with commands."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def message_to_command(self, message: str) -> object:

        sim_arr = self.sim.message_x_command_sim(message.content[22:], self.command_vectors, saved_command_vectors=True)
        picked_command_str = self.calls[int(np.argmax(sim_arr))]

        print('>message: {}\n>command calls: {}\n>similarities: {}'.format(message.content[22:], self.calls, sim_arr))

        if np.max(sim_arr) < 0.5:
            return None

        for command_str, command in self.commands.items():
            if command.call == picked_command_str:
                command.client = self.client
                command.message = message
                command.sim = self.sim

                return command