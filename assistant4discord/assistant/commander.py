from assistant4discord.nlp_tasks.similarity import Similarity
from importlib import import_module
import os
import inspect
import numpy as np


class Commander:

    def __init__(self, client, model_name, dir_path=None):
        self.client = client                                                # discord client from MyClient
        self.commands = self.get_commands(dir_path)                         # dict of commands from commands dir, {command: 'command text', ...}
        self.calls = self.get_command_calls()                               # list of commands texts, [command text, ...]
        self.sim = Similarity(model_name)                                   # w2v model class
        self.command_vectors = self.sim.get_sentence2vec(self.calls)        # calculate command text sentence vectors from self.calls

    @staticmethod
    def get_commands(dir_path) -> dict:
        """Get all commands from directory.

        Args:
            dir_path: directory path

        Returns: dict of command objects and their calls
        """
        command_dct = {}

        if not dir_path:
            dir_path = os.path.dirname(os.path.realpath(__file__)) + '/commands'

        file_lst = os.listdir(dir_path)

        for file in file_lst:
            if file.endswith('.py') and '__init__' not in file:
                module = import_module('assistant4discord.assistant.commands.{}'.format(file[:-3]))
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj):
                        print('imported command: {}'.format(name))
                        command_dct['{}'.format(name)] = obj

        return command_dct

    def get_command_calls(self):
        command_calls = []

        for command_str, command in self.commands.items():
            command_calls.append(command().call)

        return command_calls

    def message_to_command(self, message: str) -> object:

        sim_arr = self.sim.message_x_command_sim(message.content[22:], self.command_vectors, saved_command_vectors=True)

        print('command calls: {} \nsimilarities: {}'.format(self.calls, sim_arr))

        picked_command_str = self.calls[int(np.argmax(sim_arr))]

        for command_str, command in self.commands.items():
            if command().call == picked_command_str:
                command_obj = command(client=self.client, message=message, similarity=self.sim)
                return command_obj

        return None


# C = Commander(client='hey', model_name='5days_askreddit_model.kv')
# print(C.message_to_command('whats my ping'))
