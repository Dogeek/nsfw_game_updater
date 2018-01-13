import json
import os
import re

import requests
from bs4 import BeautifulSoup


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

# Download links for insexsity are just http://insexsity.com/$VERSION_$OS_64_(U).zip
# so they can be easily generated.
# Note: insexsity calls the OS "windows" "PC"
def update_insexsity_download_links(old_version, new_version):
    json_list = []
    for sub_array in load_json():
        if sub_array["game"].lower() == "insexsity":
            for opsys in ["windows", "mac", "android"]:
                sub_array["download_link_{}".format(opsys)] = sub_array["download_link_{}".format(opsys)].replace(old_version, new_version)
        json_list.append(sub_array)
    write_json_game_db(json_list)
    

def update_json_version(game_name, new_version):
    json_list = []
    for sub_array in load_json():
        if sub_array["game"].lower() == game_name.lower():
            sub_array["latest_version"] = new_version
        json_list.append(sub_array)
    write_json_game_db(json_list)
    

def get_page(page):
    return requests.get(page)

def get_page_to_check(game_name):
    for i in load_json():
        if i["game"].lower() == game_name.lower():
            return i["public_build"]
    print("Could not get page")
    return None

def get_game_latest_version(game_name):
    for i in load_json():
        if i["game"].lower() == game_name.lower():
            return str(i["latest_version"])

def insexsity():
    r = get_page(get_page_to_check("insexsity"))
    soup = BeautifulSoup(r.text, "lxml")
    version = soup.find("div", {"class": "container-fluid"}).find("div", {"class": "warringText"}).get_text().replace("Current version- ", "")
    version_on_disk = get_game_latest_version("insexsity")
    if str(version) != version_on_disk:
        print("There is a new version of insexsity")
        update_json_version("insexsity", version)
        update_insexsity_download_links(version_on_disk, version)

def trials_in_tainted_space():
    game_name = "trials in tainted space"
    link = get_current_download_link(game_name, "linux")
    if link is None:
        print("Unable to get download link for: {}".format(game_name))
    r = requests.get(link, stream=True)
    version = get_game_download_title(r).replace("TiTS_", "").replace(".swf", "")
    get_game_latest_version(game_name)
    if str(version) != get_game_latest_version(game_name):
        print("There is a new version of {}".format(game_name))
        update_json_version(game_name, version)
