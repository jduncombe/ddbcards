from dndtypes.__common import *

def calc_ac(baseac, modifiers):
    if modifiers is not None and len(modifiers) > 0:
        return baseac + modifiers[0]['value']
    return baseac

def calc_stealth(stealth):
    stealth_vals = ["Advantage", "Normal", "Disadvantage"]
    return stealth_vals[stealth]

def convert_armor(raw):
    converted = []
    for armor in raw:
        content = [
        "subtitle | {subtitle}".format(subtitle=generate_subtitle(armor['definition']['type'])),
        "rule",
        "property | AC | {ac}".format(ac=calc_ac(armor['definition']['armorClass'], armor['definition']['grantedModifiers'])),
        "property | Strength required | {strength}".format(strength=armor['definition']['strengthRequirement']),
        "property | Stealth | {stealth}".format(stealth=calc_stealth(armor['definition']['stealthCheck'])),
        "rule",
    ]
        content.extend(get_description(armor['definition']['description']))
        convertedarmor={
    "count": 1,
    "color": "dimgray",
    "icon": "breastplate",
    "title": armor['definition']['name'],
    "card_font_size": "8",
    "title_size": "11",
    "contents": content
}
        converted.append(convertedarmor)
    return converted