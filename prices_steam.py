import requests
import json

class steam_data():
    API_STEAM_ID = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json'
    PRE_URL = "https://store.steampowered.com/api/appdetails/?cc=ARS&appids="
    games_ids = {}
    
    def __init__(self):
         print("class steam_data created")
    
    @classmethod
    def parser_Ids_Steam(cls):
        list_of_json = ""
        steamData = {}
        try:
            responseSteam = requests.get(cls.API_STEAM_ID).text
            # convert from str to json and extract data of the key:applist, finally
            # extract "list" of the key:apps -> finally, this is convert to dictionary {}
            list_of_json = json.loads(responseSteam)["applist"]["apps"]
        except Exception as e:
            print(f'Exception - {e} , {type(e)}')
            
        
        for green_data_game in list_of_json:
            # the format is NameGame : IdGame, but is interchangeable.
            steamData[green_data_game["name"]] = str(green_data_game["appid"])
        
        cls.games_ids = steamData
        print("games_id updated")
        return steamData

    
    def get_price_id(self, idemt):
        idemt = str(idemt)
        completeurl = steam_data.PRE_URL + idemt
        gendrs = "| "
        categor = "| "
        result = "noting"
        try:
            dataGameSteam = json.loads(requests.get(completeurl).text)[idemt]["data"]
            for gen in dataGameSteam["genres"]:
                gendrs += gen["description"] + " | "
                
            for cate in dataGameSteam["categories"]:
                categor += cate["description"] + " | "

            result = f'''
            Name: {str(dataGameSteam["name"])}
            Current value: {str(dataGameSteam["price_overview"]["final_formatted"])}
            Controller support: {dataGameSteam["controller_support"]}
            Spanish language: {"Yes" if ("Español" in dataGameSteam["supported_languages"]
                                or "Spanish" in dataGameSteam["supported_languages"]) else "No"}
            genders: {gendrs}
            categories: {categor}
            '''
        except Exception as e:
            print(f'Exception in class: steam_data-get_price_id - {e} , {type(e)}')
            
        return result
    
    def get_price_name(self,name):
        name = str(name)
        id_game = "-1"
        completeurl = ""
        gendrs = "| "
        categor = "| "
        result = ""
        try:
            id_game = steam_data.games_ids[name]
            completeurl = steam_data.PRE_URL + id_game
            dataGameSteam = json.loads(requests.get(completeurl).text)[id_game]["data"]
            for gen in dataGameSteam["genres"]:
                gendrs += gen["description"] + " | "
                
            for cate in dataGameSteam["categories"]:
                categor += cate["description"] + " | "

            result = f'''
            Name: {str(dataGameSteam["name"])}
            Current value: {str(dataGameSteam["price_overview"]["final_formatted"])}
            Controller support: {dataGameSteam["controller_support"]}
            Spanish language: {"Yes" if ("Español" in dataGameSteam["supported_languages"]
                                or "Spanish" in dataGameSteam["supported_languages"]) else "No"}
            genders: {gendrs}
            categories: {categor}
            '''
        except Exception as e:
             print(f'Exception in class: steam_data-get_price_name - {e} , {type(e)}')
        
        return result
    

"""
test = steam_data()
print(steam_data.games_ids)
steam_data.parser_Ids_Steam()

print("POR ID")
print(test.get_price_id(203160))
print("FIN ID")
print("POR NAME")
print(test.get_price_name("Tomb Raider"))
print("FIN NAME")
"""