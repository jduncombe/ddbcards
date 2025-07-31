from dndtypes.__common import *

def get_damage(baseDamage, modifiers, type):
    if modifiers is not None and len(modifiers) > 0 and modifiers[0]['value'] is not None:
        return "{dice}+{modifier} {type}".format(type=type, modifier=modifiers[0]['value'],dice=baseDamage['diceString']) 
    return "{dice} {type}".format(type=type, dice=baseDamage['diceString']) 

def convert_weapons(raw):
    converted = []
    for weapon in raw:
        content = [
        "subtitle | {subtitle}".format(subtitle=generate_subtitle(weapon['definition']['type'])),
        "rule",
        "property | Damage | {damage}".format(damage=get_damage(weapon['definition']['damage'], weapon['definition']['grantedModifiers'], weapon['definition']['damageType'])),
        "property | Properties | {properties}".format(properties=get_item_properties(weapon['definition']['properties'], [str(weapon['definition']['range']), str(weapon['definition']['longRange'])])),
        "rule",
    ]
        content.extend(get_prop_descriptions(weapon['definition']['properties']))
        convertedweapon={
    "count": 1,
    "color": "gray",
    "title": weapon['definition']['name'],
    "card_font_size": "8",
    "title_size": "11",
    "icon": "mixed-swords",
    "contents": content
}
        converted.append(convertedweapon)
    return converted