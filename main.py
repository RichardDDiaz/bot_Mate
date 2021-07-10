import discord
from discord.ext import commands
from foreign_exchange import Foreign_exchange
from prices_steam import steam_data

bot = commands.Bot(command_prefix='_',
                   description="this is a BotMate", help_command=None)
base_change = Foreign_exchange("USD", "ARS")
base_steam = steam_data()
base_steam.parser_Ids_Steam()


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="Cotizaciones"))


@bot.command(name="dollar")
async def dollar(ctx):
    print("request data dollar.")
    await ctx.send(base_change.exchange_rate())


@bot.command(name="priceid")
async def priceid(ctx, arg):
    print("price_game_for_id.")
    await ctx.send(base_steam.get_price_id(arg))


@bot.command(name="help")
async def help(ctx):
    text = """
    Commands Bot Mate:
    > dollar: the bot says the price of the dollar in pesos
    > help: list all commands
    > prefix: _

    made with love in python :D.

    """
    await ctx.send(text)

bot.run('here write your key')
