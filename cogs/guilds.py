from ext import ExtCog

class Guilds(ExtCog):
    def __init__(self, bot):
        self.bot = bot
        self.townships = {} # id: Township
    
        self._actions = {}
    

    