from bot.bot import MafiaBot

if __name__ == "__main__":
    bot = MafiaBot()
    bot.run(bot.bot_config.pop('token'))