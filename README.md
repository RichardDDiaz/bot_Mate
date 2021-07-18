# BotMate
## _a bot to consult prices from Argentina to the rest of the world_

Mate bot is a cute non-profit bot to stay informed about:

- Price of the dollar with all current taxes
- Prices of steam games in argentina 

developed with python and discord for developers

## Environment
The project is built and tested to run in Linux system but could run in iOS and Windows.
All the commands described next in the README are aimed to Linux system.

## Prepare the bot
### Requires
you need [python 3.8.5](https://www.python.org/downloads/) or higher and pip 21.1.3 or higher. In case you don't have them you can install it with the following terminal commands
```sh
$sudo apt-get install python3.8
$sudo apt-get install python3-pip
```
- Then you need to enter [discord for developers](https://discord.com/developers/applications) and we register with our account
- Click on **new application**, write the name and click on **create**.
- On the left side we select the **Bot** option.
- We create the BOT, clicking on the **Add Bot** button and **Yes, do it!**.
- In the left menu we go to **OAuth2**. There we are going to select as Scope «bot» and as permissions «Administrator»
- This will generate a url (the one marked with the red arrow in the image), that is the one that we must copy and paste in the browser to add the bot to our server
- To obtain the token, we go to the **Bot** section and then click on **Copy**.
- Within the downloaded repository we go to the main.py file and paste the token in the last line of code within two quotes.
- > bot.run('paste your token here')
- Save and close.

## Start bot server
```sh
$pip3 install -r requiements.txt
$python3 main.ṕy
```

## References
[discord library for python](https://pypi.org/project/discord.py/)
[API steam](http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json)
[cambio today](https://cambio.today/), pagina de divisas de monedas

