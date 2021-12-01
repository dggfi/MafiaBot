class Township:
    save_table = 'townships'
    save_attrs = [
        'guild_id',
        'ch_lobby_id',
        'ch_main_id',
        'ch_crime_id',
        'ch_graveyard_id',
        'rl_player_id',
        'rl_trusted_id',
        'n_games',
        'n_players',
        'n_townie_wins',
        'n_mafia_wins',
        'n_other_wins'
    ]

    @property
    def guild_id(self):
        return self.guild.id if self.guild else None
    
    @property
    def ch_lobby_id(self):
        return self.ch_lobby.id if self.ch_lobby else None
    
    @property
    def ch_main_id(self):
        return self.ch_main.id if self.ch_main else None
    
    @property
    def ch_crime_id(self):
        return self.ch_crime.id if self.ch_crime else None
    
    @property
    def ch_graveyard_id(self):
        return self.ch_graveyard.id if self.ch_graveyard else None
    
    @property
    def rl_player_id(self):
        return self.rl_player.id if self.rl_player else None
    
    @property
    def rl_trusted_id(self):
        return self.rl_trusted.id if self.rl_trusted else None

    def __init__(self, guild):
        self.guild= guild
        
        # Channels
        self.ch_lobby = None
        self.ch_main = None
        self.ch_crime = None
        self.ch_graveyard = None
        
        # Roles
        self.rl_player = None
        self.rl_trusted = None

        # Game
        self.lobby = None

        # Metrics
        self.n_games = 0
        self.n_players = 0
        self.n_townie_wins = 0
        self.n_mafia_wins = 0
        self.n_other_wins = 0

    
    def configure(self, snowflakes, bot):
        self.guild = bot.get_guild(snowflakes['guild_id'])

        if self.guild:
            self.ch_lobby = bot.get_channel(snowflakes['lobby_channel_id'])
            self.ch_main = bot.get_channel(snowflakes['main_channel_id'])
            self.ch_crime = bot.get_channel(snowflakes['crime_channel_id'])
            self.ch_graveyard = bot.get_channel(snowflakes['graveyard_channel_id'])

            self.rl_player = bot.get_channel(snowflakes['player_role_id'])
            self.rl_trusted = bot.get_channel(snowflakes['trusted_role_id'])
        else:
            print(f"Warning: No guild set for township {self}")