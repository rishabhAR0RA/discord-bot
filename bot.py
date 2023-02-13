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

    @bot.command(
        brief="The bot will respond with the message 'Hi there!'",
        help="Example: !hello",
    )
    async def hello(ctx):
        """The bot will respond with the message 'Hi there!'"""
        await ctx.send("Hi there!")

    @bot.event
    async def on_ready():
        """
        Startup Information
        It prints out the bot's name, ID, and that it's running.
        """

        await bot.change_presence(activity=discord.Game("Going through Infinity"))
        print(f"Connected to bot: {bot.user}")

    @bot.command(brief="Adds given numbers in N N format.", help="Example: !add 1 2 3")
    async def add(ctx, *args: int):
        """Adds given numbers in N N format."""
        result = 0
        for i in args:
            try:
                result += int(i)
            except ValueError:
                await ctx.send("Please input only numbers!")
                return
        await ctx.send(f"Result : {result}")

    @bot.command(brief="Rolls a dice in N N format.", help="Example: !roll 2 6")
    async def roll(ctx, dice: str):
        """Rolls a dice in N N format."""
        try:
            rolls, limit = map(int, dice.split(" "))
        except ValueError:
            await ctx.send("Format has to be in NdN!")
            return

        result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @bot.command(
        brief="Chooses between multiple choices.",
        help="Example: !choose option1 option2",
    )
    async def choose(ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))

    @bot.command(
        brief="Repeats a message multiple times.",
        help="Example: !repeat 3 this is a repeating message",
    )
    async def repeat(ctx, times: int, content="repeating..."):
        """Repeats a message multiple times."""
        try:
            if times < 0:
                raise ValueError("Cannot repeat a negative number of times!")
        except ValueError as e:
            await ctx.send(str(e))
            return

        for i in range(times):
            await ctx.send(content)

    try:
        bot.run(DISCORD_BOT_TOKEN)
    except discord.errors.LoginFailure as e:
        print(f"Error: Login failure - {e}")
    except Exception as e:
        print(f"Error: Unexpected exception - {e}")


if __name__ == "__main__":
    run_discord_bot()
