from .helpers.master import Master
from a4d.nlp_tasks.message_processing import word2vec_input


class Word2WordSim(Master):

    def __init__(self):
        super().__init__()
        self.help = (
            "```***Word2wordSim help***\n"
            "Return cosine similarity between last two words in message.\n"
            "Call: similarity\n"
            "Example: similarity <word1>, <word2>\n"
            'Note: only works with keyword "similarity".```'
        )
        self.call = "similarity"
        self.special = {"method": "w2v"}

    async def doit(self):
        sent = word2vec_input(self.message.content)

        try:
            similarity = self.sim.model.similarity(sent[-1], sent[-2])
        except KeyError:
            await self.send("not in vocabulary")
            return

        await self.send(str(similarity))


class MostSimilarWords(Master):

    def __init__(self):
        super().__init__()
        self.help = (
            "```***MostSimilarWords help***\n"
            "Return 50 most similar words to last word in message.\n"
            "Call: most similar\n"
            "Example: similar <word>\n"
            'Note: only works with keyword "similar".```'
        )
        self.call = "most similar"
        self.special = {"method": "w2v"}

    async def doit(self):
        sent = word2vec_input(self.message.content)

        try:
            sims = self.sim.model.similar_by_word(sent[-1], topn=50)
        except KeyError:
            await self.send("not in vocabulary")
            return

        sim_str = ""
        for i in sims:
            sim_str += "{}: {:.2f} ".format(i[0], i[1])

        await self.send(sim_str)


class WordNum(Master):

    def __init__(self):
        super().__init__()
        self.help = (
            "```***WordNum help***\n"
            "How many times does a word appear in vector model.\n"
            "Call: number"
            "Example: number <word>\n"
            "Note: all words 10+ as set by model. Numbers replaced by stevilka.```"
        )
        self.call = "number"
        self.special = {"method": "w2v"}

    async def doit(self):
        sent = word2vec_input(self.message.content)

        try:
            num = self.sim.model.vocab[sent[-1]].count
        except KeyError:
            await self.send("not in vocabulary")
            return

        await self.send(str(num))
