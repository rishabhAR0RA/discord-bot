from discord.ext import commands
import discord
import random
from os import environ as env
from dotenv import load_dotenv


def run_discord_bot():
    """
    It runs a discord bot.
    """
    load_dotenv()

    DISCORD_BOT_TOKEN = env["DISCORD_BOT_TOKEN"]

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        """
        Startup Information
        It prints out the bot's name, ID, and that it's running.
        """

        await bot.change_presence(activity=discord.Game("Going through Infinity"))
        print(f"Connected to bot: {bot.user}")

    try:
        bot.run(DISCORD_BOT_TOKEN)
    except discord.errors.LoginFailure as e:
        print(f"Error: Login failure - {e}")
    except Exception as e:
        print(f"Error: Unexpected exception - {e}")


if __name__ == "__main__":
    run_discord_bot()
