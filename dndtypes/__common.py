import re

def gen_paras(paras):
    text_blocks = []
    for para in paras:
        text_blocks.append("text | {para}".format(para=para))
    return text_blocks

def generate_subtitle(name, price=None):
    if price is not None:
        return "{name} ({price})".format(name=name, price=price)
    return "{name}".format(name=name)

def get_description(text):
    text = text.lstrip("<p>").rstrip("</p>")
    return gen_paras(text.split("</p>\r\n<p>"))

def get_properties(spell):
    print("NYI")

def get_item_properties(properties, ranges):
    props = [x['name'] for x in properties if x["name"] not in ["Ammunition", "Loading"]]
    if "Thrown" in props:
        props[props.index("Thrown")] = "Thrown ({ranges})".format(ranges="/".join(ranges))
    if "Range" in props:
        props[props.index("Range")] = "Range ({ranges})".format(ranges="/".join(ranges))
    return ", ".join(props)

def get_range(range):
    if range['rangeValue'] == 0:
        return range['origin']
    else:
        return "{distance}ft {origin}".format(distance=range['rangeValue'], origin=range['origin'])

def get_aoe(range):
    if range['aoeValue'] is None and range['aoeType'] is None:
        return ""
    else:
        return "({distance}ft {type})".format(distance=range['aoeValue'], type= range['aoeType'])
    
def get_items_by_type(source, filter):
    return [x for x in source if x["definition"]["filterType"] == filter]

def process_description(desc, notes):
    desc = re.sub(r"\[[\w/]*\]", "", desc)
    desc = re.sub(r"<[\w/]*>", "", desc)
    if notes is not None:
        return "{description} <b>({notes})</b>".format(description=desc, notes=notes)
    return desc

def get_prop_descriptions(properties):
    return["description | {name} | {description}".format(name=x["name"], description = process_description(x['description'], x["notes"])) for x in properties if x["name"] not in ["Ammunition", "Two-Handed", "Loading"] ]
    