import discord
from discord.ext import commands
from foreign_exchange import Foreign_exchange

bot = commands.Bot(command_prefix='_', description="this is a BotMate")
base_change = Foreign_exchange("USD", "ARS")


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="Cotizaciones"))


@bot.command(name="dollar")
async def dollar(ctx):
    print("request data dollar.")
    await ctx.send(base_change.exchange_rate())


bot.run("change the token")
