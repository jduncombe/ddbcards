import requests
import json
import argparse
import os
import sys
from dndtypes import *

version=0.1
base_url="https://character-service.dndbeyond.com/character/v5/character/"

def print_version():
    print("ddbcards.py v{version}".format(version=version))

def get_character_json(char_id):
    resp = requests.get("{base_url}{character_id}".format(base_url=base_url, character_id=char_id))
    if resp.status_code == 200:
        return json.loads(resp.content)
    else:
        print("error reading character data")
        sys.exit(-1)

def parse_args():
    parser = argparse.ArgumentParser(prog="ddbcards", usage="Extract item data from a dndbeyond character and generate printable cards")
    parser.add_argument('-v', '--version', action="store_true", help="Print Version Information")
    parser.add_argument('-i', '--id', action='append', help='dndbeyond character id', required=True)
    parser.add_argument('-o', '--output', type=str, default= "./out",help='Set output directory')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.version:
        print_version()
        sys.exit(0)
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    for id in args.id:
        charjson = get_character_json(id)
        name = charjson["data"]["name"].replace(" ", "")
        cardsjson = []
        raw_spells = get_spells(charjson)
        raw_inventory = charjson["data"]["inventory"]
        cardsjson.extend(convert_spells(raw_spells, 'robe'))
        cardsjson.extend(convert_weapons(get_items_by_type(raw_inventory, "Weapon")))
        cardsjson.extend(convert_armor(get_items_by_type(raw_inventory, "Armor")))
        cardsjson.extend(convert_action(charjson["data"]["actions"]))
        with open(os.path.join(args.output, name+".json"), mode="wt") as f:
            json.dump(cardsjson, f)