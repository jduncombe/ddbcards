from ..models.card import Card


class CardService:
    def __init__(self):
        self.cards = []

    def create_card(self, title, contents, options):
        new_card = Card(title=title, contents=contents, options=options)
        self.cards.append(new_card)
        return new_card

    def update_card(self, card_id, title=None, contents=None, options=None):
        card = self.get_card(card_id)
        if card:
            if title is not None:
                card.title = title
            if contents is not None:
                card.contents = contents
            if options is not None:
                card.options = options
            return card
        return None

    def delete_card(self, card_id):
        card = self.get_card(card_id)
        if card:
            self.cards.remove(card)
            return True
        return False

    def get_card(self, card_id):
        for card in self.cards:
            if card.id == card_id:
                return card
        return None

    def get_all_cards(self):
        return self.cards.copy()


def process_json(input):
    """
    Process the input JSON to extract card data.
    This function should be implemented to convert the input JSON into a list of card dictionaries.
    """
    # Placeholder for actual processing logic
    cards = CardService()
    for item in input:
        title = item.get('title', 'Untitled')
        contents = item.get('contents', [])
        options = item
        cards.create_card(title, contents, options)
    return cards.get_all_cards()
