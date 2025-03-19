from dndtypes.__common import *

levels=["1st", "2nd", "3rd", "4th", "5th","6th", "7th", "8th", "9th"]

def get_spells(charjson):
    raw_spells = charjson["data"]["classSpells"][0]["spells"]
    return raw_spells

def generate_spell_subtitle(level, school):
    if level == 1:
        return "{school} Cantrip".format(school=school)
    return "{cardinallevel} Level {school}".format(cardinallevel=levels[level], school=school)

def get_components(components):
    comp_name = ["V", "S", "M"]
    matches = []
    for i in components:
        matches.append(comp_name[i-1])
    return ",".join(matches)

def get_spell_description(text):
    text = text.lstrip("<p>").rstrip("</p>").replace("<br />","")
    description = []
    if "<strong>At Higher Levels.</strong>" in text:
        desc = text.split("<strong>At Higher Levels.</strong>")
        paras = desc[0].split("</p>\r\n<p>")
        description.extend(gen_paras(paras))
        description.extend(["section | At Higher Levels",
                    "text | {upspell}".format(upspell=desc[1])])
    else: 
        description.extend(gen_paras(text.split("</p>\r\n<p>")))
    return description

def convert_spells(raw_spells, icon):
    converted = []
    for rawspell in raw_spells:
        content = [
        "subtitle | {subtitle}".format(subtitle=generate_spell_subtitle(rawspell['definition']['level'], school=rawspell['definition']['school'])),
        "rule",
        "property | Casting time | 1 action",
        "property | Range | {range} {aoe}".format(range=get_range(rawspell['definition']['range']), aoe=get_aoe(rawspell['definition']['range'])),
        "property | Components | {components}".format(components=get_components(rawspell['definition']['components'])),
        "rule",
    ]
        content.extend(get_spell_description(rawspell['definition']['description']))
        convertedspell={
    "count": 1,
    "color": "maroon",
    "title": rawspell['definition']['name'],
    "icon": icon,
    "card_font_size": "8",
    "title_size": "11",
    "contents": content
}
        converted.append(convertedspell)
    return converted