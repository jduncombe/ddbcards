from weasyprint import HTML
import os

def validate_card_data(card_data):
    if not isinstance(card_data, dict):
        raise ValueError("Card data must be a dictionary.")

    required_fields = ['title', 'contents', 'options']
    for field in required_fields:
        if field not in card_data:
            raise ValueError(f"Missing required field: {field}")


def format_card_title(title):
    return title.strip().title()


def format_card_contents(contents):
    return [line.strip() for line in contents.splitlines() if line.strip()]


def card_repeat(card_html, count):
    return [card_html] * count


def card_pages_split(cards, rows, cols):
    cards_per_page = rows * cols
    return [cards[i:i+cards_per_page] for i in range(0, len(cards), cards_per_page)]


def card_pages_add_padding(cards, options):
    cards_per_page = options["page_rows"] * options["page_columns"]
    last_page_cards = len(cards) % cards_per_page
    if last_page_cards != 0:
        padding = cards_per_page - last_page_cards
        cards += card_repeat('<div class="card"></div>', padding)
    return cards


def card_pages_wrap(pages, options):
    page_width = "210mm"
    page_height = "297mm"
    result = ""
    for i, page in enumerate(pages):
        style = f'style="background-color:{options["foreground_color"]};width:{page_width};height:{page_height};"'
        result += f'<page class="page page-preview" {style}>\n'
        result += '<div class="page-zoom page-zoom-preview">\n'
        result += "\n".join(page)
        result += '</div>\n</page>\n'
    return result


def card_pages_generate_style(options):
    pw = "210mm"
    ph = "297mm"
    return f"""<style>
    @page {{
        margin: 0;
        size:{pw} {ph};
        -webkit-print-color-adjust: exact;
    }}
    </style>
    """


def card_default_options():
    return {
        "foreground_color": "white",
        "background_color": "white",
        "default_color": "black",
        "default_icon_front": "",
        "default_icon_back": "",
        "default_title_size": "13",
        "default_card_font_size": "inherit",
        "page_size": "210mm,297mm",
        "page_rows": 3,
        "page_columns": 3,
        "page_zoom": 100,
        "card_arrangement": "doublesided",
        "card_size": "2.5in,3.5in",
        "card_width": "2.5in",
        "card_height": "3.5in",
        "card_count": None,
        "icon_inline": True,
        "rounded_corners": True,
        "back_bleed": "2mm,2mm",
        "back_bleed_width": "2mm",
        "back_bleed_height": "2mm",
    }


def card_pages_generate_html(card_data, options=None):
    if options is None:
        options = card_default_options()
    rows = options["page_rows"]
    cols = options["page_columns"]

    # Generate the HTML for each card
    front_cards = []
    for data in card_data:
        count = options["card_count"] or data.options.get("count", 1)
        front = data.card_generate_front(options)
        front_cards.extend(card_repeat(front, count))

    # Add padding cards so that the last page is full of cards
    front_cards = card_pages_add_padding(front_cards, options)
    # Split cards to pages
    front_pages = card_pages_split(front_cards, rows, cols)

    # Wrap all pages in a <page> element and add CSS for the page size
    result = ""
    result += card_pages_generate_style(options)
    result += card_pages_wrap(front_pages, options)
    return result

def card_repeat(card_html, count):
    return [card_html] * count

import math

def card_repeat(card_html, count):
    return [card_html] * count

def card_generate_color_style(color, options=None):
    return f'style="color:{color}; border-color:{color}; background-color:{color};"'

def card_generate_color_gradient_style(color, options=None):
    return f'style="background: radial-gradient(ellipse at center, white 20%, {color} 120%)"'

def add_size_to_style(style, width, height):
    # style: 'style="color:red;"'
    style = style.rstrip('"') + f";width:{width};height:{height}\""
    return style

def add_margin_to_style(style, options):
    # style: 'style="color:red;"'
    style = style.rstrip('"') + f'margin: -webkit-calc({options["back_bleed_height"]} / 2) -webkit-calc({options["back_bleed_width"]} / 2);' + '"'
    return style

def card_generate_empty(count, options):
    style_color = card_generate_color_style("white", options)
    card_style = add_size_to_style(style_color, options["card_width"], options["card_height"])
    result = f'<div class="card" {card_style}></div>'
    return card_repeat(result, count)

def card_pages_split(data, rows, cols):
    cards_per_page = rows * cols
    return [data[i:i+cards_per_page] for i in range(0, len(data), cards_per_page)]

def card_pages_merge(front_pages, back_pages):
    result = []
    for i in range(len(front_pages)):
        result.append(front_pages[i])
        result.append(back_pages[i])
    return result

def card_pages_add_padding(cards, options):
    cards_per_page = options["page_rows"] * options["page_columns"]
    last_page_cards = len(cards) % cards_per_page
    if last_page_cards != 0:
        return cards + card_generate_empty(cards_per_page - last_page_cards, options)
    else:
        return cards

def card_pages_interleave_cards(front_cards, back_cards, options):
    result = []
    i = 0
    while i < len(front_cards):
        result.append(front_cards[i])
        result.append(back_cards[i])
        if options["page_columns"] > 2:
            result += card_generate_empty(options["page_columns"] - 2, options)
        i += 1
    return result

def card_pages_interleave_cards_alt(front_cards, back_cards, options):
    result = []
    i = 0
    while i < len(front_cards):
        if i % 2:
            result.append(back_cards[i])
            result.append(front_cards[i])
        else:
            result.append(front_cards[i])
            result.append(back_cards[i])
        if options["page_columns"] > 2:
            result += card_generate_empty(options["page_columns"] - 2, options)
        i += 1
    return result

def card_pages_wrap(pages, options):
    # For simplicity, always portrait
    page_width = options.get("page_width", "210mm")
    page_height = options.get("page_height", "297mm")
    result = ""
    for i, page in enumerate(pages):
        style = f'style="background-color:{options.get("foreground_color", "white")};"'
        style = add_size_to_style(style, page_width, page_height)
        z = float(options.get("page_zoom", 100)) / 100
        zoom_style = f'style="transform: scale({z});"'
        zoom_style = add_size_to_style(zoom_style, page_width, page_height)
        result += f'<page class="page page-preview" {style}>\n'
        result += f'<div class="page-zoom page-zoom-preview" {zoom_style}>\n'
        result += "\n".join(page)
        result += '\n</div>\n</page>\n'
    return result

def card_pages_generate_style(options):
    page_width = options.get("page_width", "210mm")
    page_height = options.get("page_height", "297mm")
    result = "<style>\n"
    result += "@page {\n"
    result += "    margin: 0;\n"
    result += f"    size:{page_width} {page_height};\n"
    result += "    -webkit-print-color-adjust: exact;\n"
    result += "}\n"
    result += "</style>\n"
    return result

def card_pages_generate_html(card_data, options):
    rows = int(options.get("page_rows", 3))
    cols = int(options.get("page_columns", 3))

    front_cards = []
    back_cards = []
    for data in card_data:
        count = options.get("card_count") or data.options.get("count", 1)
        front = data.card_generate_front(options)
        back = data.card_generate_back(options)
        front_cards.extend(card_repeat(front, count))
        back_cards.extend(card_repeat(back, count))

    pages = []
    arrangement = options.get("card_arrangement", "doublesided")
    if arrangement == "doublesided":
        front_cards = card_pages_add_padding(front_cards, options)
        back_cards = card_pages_add_padding(back_cards, options)
        front_pages = card_pages_split(front_cards, rows, cols)
        back_pages = card_pages_split(back_cards, rows, cols)
        pages = card_pages_merge(front_pages, back_pages)
    elif arrangement == "front_only":
        cards = card_pages_add_padding(front_cards, options)
        pages = card_pages_split(cards, rows, cols)
    elif arrangement == "side_by_side":
        cards = card_pages_interleave_cards(front_cards, back_cards, options)
        cards = card_pages_add_padding(cards, options)
        pages = card_pages_split(cards, rows, cols)
    elif arrangement == "side_by_side_alt":
        cards = card_pages_interleave_cards_alt(front_cards, back_cards, options)
        cards = card_pages_add_padding(cards, options)
        pages = card_pages_split(cards, rows, cols)

    result = ""
    result += card_pages_generate_style(options)
    result += card_pages_wrap(pages, options)
    return result

def generate_output_html(cards):
    """
    Generates the HTML content for the RPG cards output page.

    Args:
        cards (list): A list of card dictionaries containing card data.

    Returns:
        str: The generated HTML content as a string.
    """
    card_html = card_pages_generate_html(cards, options=card_default_options())

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>RPG Cards</title>
        <!-- Javascript -->
        <script type="text/javascript" src="js/output.js"></script>
        <!-- Fonts -->
        <link href='https://fonts.googleapis.com/css?family=Noto+Sans:400,700,400italic,700italic' rel='stylesheet' type='text/css'>
        <link href='https://fonts.googleapis.com/css?family=Lora:700' rel='stylesheet' type='text/css'>
        <link href="fonts/game-icons.css" rel="stylesheet" />
        <!-- CSS -->
        <link rel="stylesheet" type="text/css" href="css/output.css">
        <link rel="stylesheet" type="text/css" href="css/cards.css">
        <link rel="stylesheet" type="text/css" href="css/card-size.css">
        <link rel="stylesheet" type="text/css" href="css/icons.css">
        <link rel="stylesheet" type="text/css" href="css/custom-icons.css">
        <link href="css/style.css" rel="stylesheet" />
    </head>
    <body class="page-background">
        <div class="cards-container">
            {card_html}
        </div>
        <button onclick="window.close();" id="close-button" style="display: none; margin: 50vh auto 0 auto; transform: translateY(-50%);">Close</button>
    </body>
    </html>
    """
    return html_content


def generate_pdf(cards):
    # Example: Get HTML content from the request
    card_html = generate_output_html(cards)

    # Generate PDF from HTML
    pdf = HTML(string=card_html, base_url=os.path.abspath(__file__)).write_pdf(optimize_images=True, pdf_variant="pdf/ua-2")
    return pdf 
