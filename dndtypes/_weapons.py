from dndtypes.__common import *

"""
  {
    "count": 1,
    "color": "dimgray",
    "title": "Dagger",
    "icon": "mixed-swords",
    "contents": [
      "subtitle | Simple melee weapon (2gp)",
      "rule",
      "property | Damage | 1d4 piercing",
      "property | Modifier | Strength or Dexterity",
      "property | Properties | Light, Finesse, Thrown (20/60)",
      "rule",
      "fill | 2",
      "description | Finesse | Use your choice of Strength or Dexterity modifier for attack and damage.",
      "description | Light | When you attack while dual wielding light weapons, you may use a bonus action to attack with your off hand.",
      "description | Thrown | You can throw the weapon to make a ranged attack with the given range.",
      "fill | 3"
    ],
    "tags": [
      "item",
      "weapon"
    ]
  },
"""

def get_damage(baseDamage, modifiers, type):
    if modifiers is not None:
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