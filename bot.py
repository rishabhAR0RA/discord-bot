from discord.ext import commands
import discord
import openai
import random
import requests
from os import environ as env
from dotenv import load_dotenv


def run_discord_bot():
    """
    It runs a discord bot.
    """
    load_dotenv()

    DISCORD_BOT_TOKEN = env["DISCORD_BOT_TOKEN"]  # Your token
    WEATHER_KEY = env["WEATHER_KEY"]  # Your token
    OPENAI_KEY = env["OPENAI_KEY"]  # Your token

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

    @bot.command(
        brief="Generate an image according to prompt provided",
        help="Example: !img Mango",
    )
    async def image(ctx, prompt: str):
        try:
            openai_endpoint = "https://api.openai.com/v1/images/generations"
            openai_header = {
                "Authorization": f"Bearer {OPENAI_KEY}",
                "Content-Type": "application/json",
            }
            openai_config = {
                "prompt": prompt,
            }
            openai_response = requests.post(
                url=openai_endpoint, json=openai_config, headers=openai_header
            )
            openai_data = openai_response.json()["data"][0]["url"]
            embed = discord.Embed(
                title="AI generated image",
                description=f"{prompt}",
                color=0xA6569B,
            )
            embed.set_image(url=openai_data)
            await ctx.send(embed=embed)
        except requests.exceptions.RequestException as e:
            await ctx.send(
                "Could not retrieve openai information. Please try again later."
            )

    @bot.command(
        name="weather",
        brief="Get the current weather condition for a city",
        help="Example: !weather London",
    )
    async def weather(ctx, city: str):
        try:
            weather_url = "https://api.weatherapi.com/v1/current.json"
            parameters = {
                "key": WEATHER_KEY,
                "q": city,
            }

            response = requests.get(weather_url, params=parameters)
            response.raise_for_status()

            data = response.json()
            condition = data["current"]["condition"]["text"]
            temperature = data["current"]["temp_c"]
            weather_icon_url = data["current"]["condition"]["icon"]
            humidity = data["current"]["humidity"]
            wind_kph = data["current"]["wind_kph"]
            wind_dir = data["current"]["wind_dir"]
            precip_mm = data["current"]["precip_mm"]
            localtime = data["location"]["localtime"]

            embed = discord.Embed(
                title=f"Weather in {city}",
                description=f"Current condition: {condition}",
                color=0x00FF00,
            )

            embed.set_thumbnail(url=f"https:{weather_icon_url}")
            embed.add_field(name="Temperature", value=f"{temperature}°C")
            embed.add_field(name="Humidity", value=f"{humidity}%")
            embed.add_field(
                name="Wind Speed",
                value=f"{wind_kph} kph, direction: {wind_dir}",
            )
            embed.add_field(name="Precipitation", value=f"{precip_mm} mm")
            embed.add_field(name="Local Time", value=f"{localtime}")

            await ctx.send(embed=embed)
        except requests.exceptions.RequestException as e:
            await ctx.send(
                "Could not retrieve weather information. Please try again later."
            )

    try:
        bot.run(DISCORD_BOT_TOKEN)
    except discord.errors.LoginFailure as e:
        print(f"Error: Login failure - {e}")
    except Exception as e:
        print(f"Error: Unexpected exception - {e}")


if __name__ == "__main__":
    run_discord_bot()
