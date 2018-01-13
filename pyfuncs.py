import json
import re
import os

def load_json():
    with open('games.json', 'r') as jsonfile:
        return json.loads(jsonfile.read())

def get_current_download_link(game, os):
    link = ""
    for i in load_json():
        if i["game"].lower() == game.lower():
            return i["download_link_" + os]
    return None

def get_game_download_title(r):
    try:
        d = r.headers['content-disposition']
        return re.findall("filename=(.+)", d)[0]
    except KeyError:
        return None

def write_json_game_db(json_list):
    with open('temp_json', 'w', encoding="utf-8") as f:
         f.write(json.dumps(json_list, indent=4, sort_keys=True))
    os.remove("games.json")
    os.rename("temp_json", "games.json")

def update_json_version(game_name, new_version):
    json_list = []
    for sub_array in load_json():
        if sub_array["game"].lower() == game_name.lower():
            sub_array["latest_version"] = new_version
        json_list.append(sub_array)
    write_json_game_db(json_list)