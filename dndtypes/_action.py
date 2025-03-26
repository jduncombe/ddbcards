from dndtypes.__common import *

def convert_action(raw):
    converted = []
    for type in ["race", "class", "background", "item", "feat"]:
        if raw[type] is not None:
            for typedaction in raw[type]:
                content = [
                    "subtitle | {subtitle} option".format(subtitle=generate_subtitle(type)),
                    "rule",
                ]
                content.extend(get_description(typedaction['snippet']))
                convertedaction={
            "count": 1,
            "color": "LightSlateGray",
            "icon": "skills",
            "title": typedaction['name'],
            "card_font_size": "8",
            "title_size": "11",
            "contents": content
        }
                converted.append(convertedaction)
    return converted