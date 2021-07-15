import discord
from discord.ext import commands
from foreign_exchange import Foreign_exchange
from prices_steam import steam_data

# initializer bot
bot = commands.Bot(command_prefix='_',
                   description="this is a BotMate", help_command=None)
print("initializing the bot...")
base_change = Foreign_exchange("USD", "ARS")
base_steam = steam_data()
base_steam.parser_Ids_Steam()
print("ready...")

'''
bot initializer: set the status of the bot to be displayed when it is online
'''
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="Cotizaciones"))


'''
consult the price of dollar in pesos.
'''
@bot.command(name="dollar")
async def dollar(ctx):
    print("request data dollar.")
    await ctx.send(base_change.exchange_rate())

'''
consult the price of game in steam according to his id_game
'''
@bot.command(name="priceid")
async def priceid(ctx, arg):
    print(f"price_game_for_id: {str(arg)}")
    await ctx.send(base_steam.get_price_id(arg))

'''
consult the price of game in steam according to his name
'''
@bot.command(name="pricename")
async def pricename(ctx, *args):
    args = list(args)
    for pal in args:
        pal = str(pal)
    args = " ".join(args)
    print(f"price_game_for_name: {args}")
    await ctx.send(base_steam.get_price_name(args))

'''
listing commands implemented in botMate
'''
@bot.command(name="help")
async def help(ctx):
    text = """
    Commands Bot Mate:
    > dollar: says the price of the dollar in pesos
    > priceid: says the price of a game by its id in steam
    > pricename: says the price of a game by name on steam
    > help: list all commands
    > prefix: _

    made with love in python :D.

    """
    await ctx.send(text)

# Your token here. Extract from Discord developers
bot.run('ODYzMDUwNDE2NDEyMTY0MTM2.YOhQVQ.LyXWuks3VVDdqcILu8MbeREZOGI')
