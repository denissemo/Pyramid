"""
Created on: 18.02.2018
"""
from deck import DeckGenerator
from deck import Card


class TableCard:
    """Contain pyramid deck and additional deck."""

    def __init__(self, deck):
        """
        Initializing class.

        :param deck: DeckGenerator object
        """
        assert isinstance(deck, DeckGenerator), 'deck object incorrect'

        self._current_deck = deck
        self._pyramid = []
        self._pyramid_rows = 7

    def generate_pyramid(self):
        """Generate pyramid."""
        self._pyramid = [[self._current_deck.deck.pop() for j in range(i)]
                         for i in range(1, self._pyramid_rows+1)]

    @property
    def additional_deck(self):
        """Return additional deck object."""
        return self._current_deck

    @property
    def pyramid_deck(self):
        """Return pyramid list."""
        return self._pyramid

    def isPyramidCard(self, card_obj):
        """Check if is a Card object.
        :return: bool """
        assert isinstance(card_obj, Card), 'incorrect Card object'

        if card_obj in self._current_deck.deck:
            return False
        for row in self._pyramid:
            if card_obj in row:
                return True

    def __getitem__(self, item):
        """Return item from deck.

        :param item: Card object"""
        assert isinstance(item, Card), 'incorrect Card object'
        if item in self._current_deck.deck:
            return item
        for row in self._pyramid:
            if item in row:
                return item
        return None

    def __str__(self):
        """Return pyramid in readable style."""
        res = ''
        for row in self._pyramid:
            for card in row:
                res += '|{}-{}-{}|'.format(card.rank, card.suit,
                                           'Open' if card.status else 'Close') \
                       + ' '
            res += '\n'
        return res


def test():
    # ---------------- Test ----------------
    d = DeckGenerator()
    d.shuffle()
    t = TableCard(d)
    t.generate_pyramid()
    c = p.pyramid_deck[1][1]
    del p[c]
    print(t)

    for i in p.pyramid_deck[-1]:
        i.open()
    print(p)


if __name__ == '__main__':
    test()
