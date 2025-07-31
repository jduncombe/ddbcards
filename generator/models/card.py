class Card:
    def __init__(self, title, contents, options=None):
        self.title = title
        self.contents = contents
        self.options = options if options is not None else {}

    def to_dict(self):
        return {
            'title': self.title,
            'contents': self.contents,
            'options': self.options
        }

    def card_generate_color_style(self, color):
        return f'style="color:{color}; border-color:{color}; background-color:{color}"'

    def add_size_to_style(self, style, width, height):
        style = style.rstrip('"') + f";width:{width};height:{height}\""
        return style
    
    def card_element_title(self, options):
        title = self.title
        title_size = self.options.get("title_size", options.get("default_title_size", "normal"))
        return f'<div class="card-title card-title-{title_size}">{title}</div>'

    def card_element_icon(self, options):
        icons = self.options.get("icon", options.get("default_icon_front", "")).split()
        classname = "inlineicon" if options.get("icon_inline", True) else "icon"
        result = f'<div class="card-title-{classname}-container">'
        for icon in icons:
            result += f'<img class="card-title-{classname} icon-{icon}" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">'
        result += '</div>'
        return result

    def card_element_subtitle(self, params, options = None):
        subtitle = params[0] if len(params) > 0 else ""
        result = '<div class="card-element card-subtitle">'
        if len(params) > 1 and params[1]:
            result += f'<div style="float:right">{params[1]}</div>'
        result += f'<div>{subtitle}</div>'
        result += '</div>'
        return result

    def card_element_inline_icon(self, params, options):
        icon = params[0] if len(params) > 0 else ""
        size = params[1] if len(params) > 1 else "40"
        align = params[2] if len(params) > 2 else "center"
        color = self.options.get("color_front", self.options.get("color", options.get("default_color", "black")))
        return f'<div class="card-element card-inline-icon align-{align} icon-{icon}" style="height:{size}px;min-height:{size}px;width:{size}px;background-color:{color}"></div>'

    def card_element_picture(self, params, options):
        url = params[0] if len(params) > 0 else ""
        height = params[1] if len(params) > 1 else ""
        return f'<div class="card-element card-picture" style="background-image: url(&quot;{url}&quot;); background-size: contain; background-position: center;background-repeat: no-repeat; height:{height}px"></div>'

    def card_element_ruler(self, params, options):
        color = self.options.get("color_front", self.options.get("color", options.get("default_color", "black")))
        card_font_size_class = self.card_size_class(options)
        return (
            f'<svg class="card-ruler{card_font_size_class}" height="1" width="100" viewbox="0 0 100 1" preserveaspectratio="none" xmlns="http://www.w3.org/2000/svg">'
            f'<polyline points="0,0 100,0.5 0,1" fill="{color}"></polyline>'
            f'</svg>'
        )

    def card_element_boxes(self,params, options):
        color = self.options.get("color_front", self.options.get("color", options.get("default_color", "black")))
        count = int(params[0]) if len(params) > 0 else 1
        size = params[1] if len(params) > 1 else 3
        additional_text = params[2] if len(params) > 2 else ""
        style = f'style="width:{size}em;height:{size}em"'
        element_class = self.card_element_class(options)
        result = f'<div class="{element_class}">'
        for _ in range(count):
            result += (
                f'<svg class="card-box" height="100" width="100" viewbox="0 0 100 100" preserveaspectratio="none" xmlns="http://www.w3.org/2000/svg" {style}>'
                f'<rect x="5" y="5" width="90" height="90" fill="none" stroke="{color}" style="stroke-width:10"></rect>'
                f'</svg>'
            )
        result += additional_text + '</div>'
        return result

    def card_element_property(self, params, options):
        card_font_size_class = self.card_size_class(options)
        result = f'<div class="card-element card-property-line{card_font_size_class}">'
        result += f'<h4 class="card-property-name">{params[0]}</h4>'
        result += f'<p class="card-p card-property-text">&nbsp;{params[1]}</p>'
        if len(params) > 2 and params[2]:
            result += '<div style="float:right">'
            result += f'<h4 class="card-property-name">{params[2]}</h4>'
            result += f'<p class="card-p card-property-text">{params[3]}</p>'
            result += '</div>'
        result += '</div>'
        return result

    def card_element_text(self, params, options):
        element_class = self.card_element_class(options)
        return f'<div class="{element_class}"><p class="card-p card-description-text">{params[0]}</p></div>'

    def card_element_center(self, params, options):
        element_class = self.card_element_class(options)
        return f'<div class="{element_class}" style="text-align: center"><p class="card-p card-description-text">{params[0]}</p></div>'

    def card_element_justify(self, params, options):
        element_class = self.card_element_class(options)
        return f'<div class="{element_class}" style="text-align: justify; hyphens: auto"><p class="card-p card-description-text">{params[0]}</p></div>'

    def card_element_bullet(self, params, options):
        card_font_size_class = self.card_size_class(options)
        return f'<ul class="card-element card-bullet-line{card_font_size_class}"><li class="card-bullet">{params[0]}</li></ul>'

    def card_element_section(self, params, options):
        color = self.options.get("color_front", self.options.get("color", options.get("default_color", "black")))
        section = params[0] if len(params) > 0 else ""
        result = f'<h3 class="card-section" style="color:{color}">'
        if len(params) > 1 and params[1]:
            result += f'<div style="float:right">{params[1]}</div>'
        result += f'<div>{section}</div></h3>'
        return result

    def card_element_fill(self, params, options):
        flex = params[0] if len(params) > 0 else "1"
        return f'<span class="card-fill" style="flex:{flex}"></span>'

    def card_element_unknown(self, params, options):
        return f'<div>Unknown element: {"<br />".join(params)}</div>'

    def card_element_empty(self, params, options):
        return ''

    # Helper functions
    def card_element_class(self, options):
        card_font_size_class = self.card_size_class(options)
        return f'card-element card-description-line{card_font_size_class}'

    def card_size_class(self, options):
        card_font_size = self.options.get("card_font_size", options.get("default_card_font_size", ""))
        return f' card-font-size-{card_font_size}' if card_font_size and card_font_size != "inherit" else ''

    def card_element_dndstats(self, params, options):
        stats = [int(params[i]) if i < len(params) and params[i].isdigit() else 10 for i in range(6)]
        mods = []
        for stat in stats:
            mod = (stat - 10) // 2
            mods.append(f"&nbsp;({mod:+d})")
        card_font_size_class = self.card_size_class(options)
        result = ""
        result += f'<table class="card-stats{card_font_size_class}">'
        result += '    <tbody><tr>'
        result += '      <th class="card-stats-header">STR</th>'
        result += '      <th class="card-stats-header">DEX</th>'
        result += '      <th class="card-stats-header">CON</th>'
        result += '      <th class="card-stats-header">INT</th>'
        result += '      <th class="card-stats-header">WIS</th>'
        result += '      <th class="card-stats-header">CHA</th>'
        result += '    </tr>'
        result += '    <tr>'
        for i in range(6):
            result += f'      <td class="card-stats-cell">{stats[i]}{mods[i]}</td>'
        result += '    </tr>'
        result += '  </tbody>'
        result += '</table>'
        return result

    def card_element_swstats(self, params, options):
        stats = [params[i] if i < len(params) else '-' for i in range(9)]
        card_font_size_class = self.card_size_class(options)
        result = ""
        result += f'<table class="card-stats{card_font_size_class}">'
        result += '    <tbody><tr>'
        result += '      <th class="card-stats-header">Agility</th>'
        result += '      <th class="card-stats-header">Smarts</th>'
        result += '      <th class="card-stats-header">Spirit</th>'
        result += '      <th class="card-stats-header">Strength</th>'
        result += '      <th class="card-stats-header">Vigor</th>'
        result += '    </tr>'
        result += '    <tr>'
        for i in range(5):
            result += f'      <td class="card-stats-cell">d{stats[i]}</td>'
        result += '    </tr>'
        result += '  </tbody>'
        result += '</table>'
        result += '<p class="card-stats-sw-derived">'
        result += f' <b>Pace</b> {stats[5]}'
        result += f' <b>Parry</b> {stats[6]}'
        result += f' <b>Toughness</b> {stats[7]}'
        if stats[8]:
            result += f' <b>Loot</b> {stats[8]}'
        result += '</p>'
        return result

    def card_element_description(self, params, options):
        element_class = self.card_element_class(options)
        name = params[0] if len(params) > 0 else ""
        desc = params[1] if len(params) > 1 else ""
        result = ""
        result += f'<div class="{element_class}">'
        result += f'   <h4 class="card-description-name">{name}</h4>'
        result += f'   <p class="card-p card-description-text">{desc}</p>'
        result += '</div>'
        return result

    # Map element names to generator functions
    CARD_ELEMENT_GENERATORS = {
        "subtitle": card_element_subtitle,
        "property": card_element_property,
        "rule": card_element_ruler,
        "ruler": card_element_ruler,
        "boxes": card_element_boxes,
        "text": card_element_text,
        "center": card_element_center,
        "justify": card_element_justify,
        "bullet": card_element_bullet,
        "section": card_element_section,
        "fill": card_element_fill,
        "disabled": card_element_empty,
        "picture": card_element_picture,
        "icon": card_element_inline_icon,
        "description": card_element_description,
        "dndstats": card_element_dndstats,
        "text": card_element_text,
        "center": card_element_center,
        "justify": card_element_justify,
        "bullet": card_element_bullet,
        "fill": card_element_fill,
        "section": card_element_section,
        "disabled": card_element_empty,
        "picture": card_element_picture,
        "icon": card_element_inline_icon
    }

    def card_data_color_front(self, options):
        return self.options.get("color_front") or self.options.get("color") or options.get("default_color", "black")

    def card_data_color_back(self, options):
        return self.options.get("color_back") or self.options.get("color") or options.get("default_color", "black")

    def card_data_icon_front(self, options):   
        return self.options.get("icon") or options.get("default_icon_front", "")

    def card_data_icon_back(self, options):
        return self.options.get("icon") or options.get("default_icon_back", "")

    def card_data_split_params(self, value):
        return [s.strip() for s in value.split("|")]

    def card_element_class(self, options):
        card_font_size_class = self.card_size_class(options)
        return f'card-element card-description-line{card_font_size_class}'

    def card_size_class(self, options):
        card_font_size = self.options.get("card_font_size") or options.get("default_card_font_size", "")
        return f' card-font-size-{card_font_size}' if card_font_size and card_font_size != "inherit" else ''

    def card_generate_contents(self, options):
        result = ""
        for value in self.contents:
            parts = [p.strip() for p in value.split("|")]
            element_name = parts[0]
            element_params = parts[1:]
            element_generator = self.CARD_ELEMENT_GENERATORS.get(element_name)
            if element_generator:
                result += element_generator(self, element_params, options)
            elif element_name:
                result += self.card_element_unknown(element_params, options)
        return f'<div class="card-content-container">{result}</div>'

    def card_generate_front(self, options):
        color = self.card_data_color_front(options)
        style_color = self.card_generate_color_style(color)
        card_size_style = self.add_size_to_style(
            style_color, options["card_width"], options["card_height"])
        card_style = card_size_style  # margin omitted for simplicity

        title_size = self.options.get("title_size", options["default_title_size"])

        result = ""
        result += f'<div class="card {"rounded-corners" if options["rounded_corners"] else ""}" {card_style}>'
        result += '<div class="card-header">'
        result += f'<div class="card-title card-title-{title_size}">{self.title}</div>'
        result += self.card_element_icon(options);
        result += '</div>'
        result += self.card_generate_contents(options)
        result += '</div>'
        return result

    def card_generate_back(self, options):
        color = self.card_data_color_back(options)
        style_color = self.card_generate_color_style(color)

        width = options["card_width"]
        height = options["card_height"]
        back_bleed_width = options["back_bleed_width"]
        back_bleed_height = options["back_bleed_height"]

        card_width = f"-webkit-calc({width} + {back_bleed_width})"
        card_height = f"-webkit-calc({height} + {back_bleed_height})"

        card_style = self.add_size_to_style(style_color, card_width, card_height)

        url = self.options.get("background_image")
        if url:
            background_style = (
                f'style="background-image: url(&quot;{url}&quot;); '
                'background-size: contain; background-position: center; background-repeat: no-repeat;"'
            )
        else:
            background_style = self.card_generate_color_style(color)

        icon = self.card_data_icon_back(options)
        # For icon size, we use a default or fixed value since we can't measure DOM elements in Python
        icon_size = "60px"
        icon_style = self.add_size_to_style(style_color, icon_size, icon_size)

        result = ""
        result += f'<div class="card {"rounded-corners" if options.get("rounded_corners") else ""}" {card_style}>'
        result += f'  <div class="card-back" {background_style}>'
        if not url:
            result += '    <div class="card-back-inner">'
            result += f'      <div class="card-back-icon icon-{icon}" {icon_style}></div>'
            result += '    </div>'
        result += '  </div>'
        result += '</div>'

        return result

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get('title'),
            contents=data.get('contents'),
            options=data.get('options', {})
        )
