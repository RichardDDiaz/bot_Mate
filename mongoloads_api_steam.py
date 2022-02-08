import requests
import json
import time
import os
from bs4 import BeautifulSoup
from pymongo import MongoClient

"""
input: id de juego
output: json con los datos del juego en formato json listo 
    para ser insertado en mongo
"""
def http_parse_json(game_id):
    # url de la pagina de steam sin parametros de busqueda
    raw_link = "https://store.steampowered.com/api/appdetails/?cc=ARS&appids="
    try:
        dataGameSteam = json.loads(
                    requests.get(raw_link + str(game_id)).text)[str(game_id)]["data"]
    except:
        return "NoData"
    
    pre_json_import = {}
    # Nombre completo del contenido
    if "name" in dataGameSteam:
        pre_json_import['name'] = dataGameSteam['name']

    # Descripcion
    if "about_the_game" in dataGameSteam:
        pre_json_import["about_the_game"] = BeautifulSoup(dataGameSteam["about_the_game"], features="html.parser").get_text()
    
    # Idioma disponibles
    if 'supported_languages' in dataGameSteam:
        pre_json_import['supported_languages'] = BeautifulSoup(dataGameSteam["supported_languages"], features="html.parser").get_text()

    # Categorias
    categories = []
    if "categories" in dataGameSteam:
        for i in dataGameSteam["categories"]:
            categories.append(i["description"])
        pre_json_import["categories"] = categories

    # Generos
    genres = []
    if "genres" in dataGameSteam:
        for i in dataGameSteam['genres']:
            genres.append(i['description'])
        pre_json_import["genres"] = genres
    
    # Soporte de controles
    if "controller_support" in dataGameSteam:
        pre_json_import["controller_support"] = dataGameSteam["controller_support"]

    # Desarolladores
    if "developers" in dataGameSteam:
        pre_json_import["developers"] = dataGameSteam["developers"]

    # Si es DLC: aqui estara el juego base
    if "fullgame" in dataGameSteam:
        pre_json_import["fullgame"] = dataGameSteam["fullgame"] 

    # Portada de fondo
    if 'header_image' in dataGameSteam:
        pre_json_import['header_image'] = dataGameSteam['header_image']

    # Requisitos de sistema
    if "pc_requirements" in dataGameSteam:
        delimiter = " |&| "
        pre_json_import['pc_requirements'] = {}

    if "minimum" in dataGameSteam["pc_requirements"]:
        soup = BeautifulSoup(dataGameSteam['pc_requirements']["minimum"], features="html.parser")
        data_list = soup.get_text(delimiter).split(delimiter)[1:]
        pre_json_import['pc_requirements']["minimum"] = {}
        for i in range(0, len(data_list)-1, 2):
            pre_json_import['pc_requirements']["minimum"][data_list[i]] = data_list[i+1] 

    if "recommended" in dataGameSteam["pc_requirements"]:
        soup = BeautifulSoup(dataGameSteam['pc_requirements']["recommended"], features="html.parser")
        data_list = soup.get_text(delimiter).split(delimiter)[1:]
        pre_json_import['pc_requirements']["recommended"] = {}

        for i in range(0, len(data_list)-1, 2):
            pre_json_import['pc_requirements']["recommended"][data_list[i]] = data_list[i+1]

    # Plataformas Compatibles:
    if "platforms" in dataGameSteam:
        pre_json_import['platforms'] = dataGameSteam['platforms']

    # Precio
    if 'price_overview' in dataGameSteam:
        pre_json_import['price_overview'] = dataGameSteam['price_overview']

    # Capturas de pantalla
    if "screenshots" in dataGameSteam:
        pre_json_import["screenshots"] = dataGameSteam["screenshots"]

    return pre_json_import


"""
descripcion: funcion que inserta los metadatos de todos los juegos
    de steam en una base de datos mongo llamada "steam"
"""
def load_data():
    API_STEAM_ID = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json'
    list_of_json = ""
    steamData = {}

    # creando un diccionario nombre juego: su id
    try:
        responseSteam = requests.get(API_STEAM_ID).text
        list_of_json = json.loads(responseSteam)["applist"]["apps"]
    except Exception as e:
        print(f'Exception - {e} , {type(e)}, please restart the script')

    for green_data_game in list_of_json:
        steamData[green_data_game["name"]] = str(green_data_game["appid"])
    
    print("iniciando carga de datos")

    #configuracion por defecto
    bd_mongo = MongoClient("localhost")

    #eliminar database si existe
    bd_mongo.drop_database("steam")

    #creando database
    steam_db = bd_mongo["steam"]

    #coleccion
    metadatos = steam_db["metadatos"]

    for i in steamData:
        ## realizar consulta http y insertar en la coleccion metadatos
        ## minimo 1.57 segundos entre cada consulta 
        ## solo podemos realizar maximo 200 consulta cada 5 minutos
        ## en el mejor caso relizariamos aproximanete 190 consultas cada 5 minutos
        inicio = time.time()
        id_game = str(steamData[i])
        try:
            metadatos.insert_one({"_id":id_game, id_game:http_parse_json(id_game)})
            print(f"add id game: {id_game}")
        except Exception as e:
            print(f'Exception mongoDB - {e} , {type(e)}, id_game: {id_game}')
            with open ("log.txt", "w") as text_file:
                text_file.write(f"Exception mongoDB - {e} , {type(e)}, id_game: {id_game}" + os.linesep)
                text_file.write("-"* 80 + os.linesep)
            continue
        time.sleep(0.0 if (time.time() - inicio) >= 1.57 else 1.57 - (time.time() - inicio))


if "__main__" == __name__:
    load_data()