import requests
import json


class NameGameNotFount(Exception):
    pass

'''
Dedicated Class from handle every data in steam
WARNING: when creating an instantiated class the class attribute 
    "games_ids" will be empty. You must call the method "parser_Ids_Steam" to 
    configure the attribute with the games with their id
'''
class steam_data():
    API_STEAM_ID = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json'
    PRE_URL = "https://store.steampowered.com/api/appdetails/?cc=ARS&appids="
    games_ids = {}

    def __init__(self):
        print("class steam_data created")

    # Obtain all games/DLC from the steam database and convert in dicc
    # Pre: nothing, Post: dicc{"x game in str" -> "your id game in str"}
    @classmethod
    def parser_Ids_Steam(cls):
        list_of_json = ""
        steamData = {}
        try:
            responseSteam = requests.get(cls.API_STEAM_ID).text
            # convert str to json and extract data of the key:applist, finally
            # extract "list" of the key:apps -> finally, this is convert to
            # dictionary {}.
            list_of_json = json.loads(responseSteam)["applist"]["apps"]
        except Exception as e:
            print(f'Exception - {e} , {type(e)}')

        for green_data_game in list_of_json:
            # the format is NameGame : IdGame, but is interchangeable.
            steamData[green_data_game["name"]] = str(green_data_game["appid"])

        cls.games_ids = steamData
        print("games_id updated")
        return steamData
    
    # Get game price in steam (pesos ARS) with your id.
    # Pre: Nothing, Pos: str with redundant information of game.
    def get_price_id(self, idemt):
        idemt = str(idemt)
        completeurl = steam_data.PRE_URL + idemt

        result = """The game could not be found.
        Please try again or write it respecting the capital letters
        """
        try:
            dataGameSteam = json.loads(
                requests.get(completeurl).text)[idemt]["data"]
            result = self.parser_price(dataGameSteam)
        except Exception as e:
            print(f'Exception in class: steam_data-get_price_id-{e}')

        return result

    # Get game price in steam (pesos ARS) with your name.
    # Pre: class attribute games_ids != {}.
    # Post: str with redundant information of game.
    def get_price_name(self, name):
        name = str(name)
        result = """The game could not be found.
        Please try again or write it respecting the capital letters
        """
        try:
            id_game = steam_data.games_ids[name]
            completeurl = steam_data.PRE_URL + id_game
            dataGameSteam = json.loads(
                requests.get(completeurl).text)[id_game]["data"]
            result = self.parser_price(dataGameSteam)
        except Exception as e:
            print(f'Exception in class: steam_data-get_price_name-{e}')

        return result
    

    # Build the redundant information of the game in steam.
    # Pre: dataGameSteam != Json Empty.
    # Post: str with redundatnt informacion of game.
    def parser_price(self, dataGameSteam):
        gendrs = "| "
        categor = "| "
        result = []
        if "genres" in dataGameSteam:
            for gen in dataGameSteam["genres"]:
                gendrs += gen["description"] + " | "

        if "categories" in dataGameSteam:
            for cate in dataGameSteam["categories"]:
                categor += cate["description"] + " | "

        if "name" in dataGameSteam:
            result.append(f'Name:{str(dataGameSteam["name"])}\n')
        
        if "price_overview" in dataGameSteam:
            result.append(f'Current value: {str(dataGameSteam["price_overview"]["final_formatted"])}\n')

        if "Español" in dataGameSteam["supported_languages"] or "Spanish" in dataGameSteam["supported_languages"]:
            result.append("Spanish language: Yes\n")
        else:
            result.append("Spanish language: No\n")

        if gendrs != "| ":
            result.append(f'Genders: {gendrs}\n')
        else:
            result.append('Categories not available\n')

        if categor != "| ":
            result.append(f'Categories: {categor}\n')
        else:
            result.append('Categories not available\n')


        return "".join(result)
