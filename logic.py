"""
Created on: 18.02.2018
"""
from deck import DeckGenerator  # only for test
from table import TableCard
from deck import Card
from functools import reduce
import copy


class GameLogic:
    """Main game logic class."""

    def __init__(self, table_obj):
        """
        Initializing class.

        :param table_obj: TableCard object
        """
        assert isinstance(table_obj, TableCard), 'incorrect table object'

        self._table_obj = table_obj
        self._level = 'easy'
        self._card_stack = []  # additional card stack
        self._changes = {'pyramid_deck': [], 'add_deck': [],  # changes journal
                         'stack': []}
        self._history = []  # history of changes

    def cardIndex(self, card_obj):
        """Return Card object index from different lists."""
        assert isinstance(card_obj, Card), 'incorrect Card object'

        # if card in add deck
        if card_obj in self._table_obj.additional_deck.deck:
            return self._table_obj.additional_deck.deck.index(card_obj)
        # if card in stack
        elif card_obj in self._card_stack:
            return self._card_stack.index(card_obj)
        # if card in pyramid deck
        for row in self._table_obj.pyramid_deck:
            if card_obj in row:
                return self._table_obj.pyramid_deck.index(row), row.index(card_obj)

    def _del_card(self, card_obj):
        """Mark card as None."""
        assert isinstance(card_obj, Card), 'incorrect Card object'

        # add copy Card object
        if self._table_obj.isPyramidCard(card_obj):
            self._changes['pyramid_deck'].append(copy.deepcopy(card_obj))
            self._history.append({'pyramid_deck': self.cardIndex(card_obj)})
        else:
            if card_obj in self._card_stack:
                self._changes['stack'].append(copy.deepcopy(card_obj))
                self._history.append({'stack': self.cardIndex(card_obj)})
            else:
                self._changes['add_deck'].append(copy.deepcopy(card_obj))
                self._history.append({'add_deck': self.cardIndex(card_obj)})

        card_obj.rank = None
        card_obj.suit = None
        card_obj.status = False

    def redo_changes(self):
        """Return redo information.

        :returns: card, card_index, card_type """
        last_del_elem = self._history.pop()  # dict
        card_type = list(last_del_elem.keys())[0]  # add_deck or pyramid_deck
        card = self._changes[card_type].pop()  # card obj
        card_index = last_del_elem[card_type]  # index of returned card
        return {'card': card, 'card_index': card_index, 'card_type': card_type}

    def compare_card(self, *args):
        """Compare and delete cards from deck."""
        assert all(list(map(lambda obj: isinstance(obj, Card), list(args)))), \
            'this is not Card object'

        if any(list(map(lambda obj: obj in self._card_stack, list(args)))):
            map(lambda obj: self._del_card(obj), list(args))
        if all(list(map(lambda obj: obj.status, list(args)))):
            if sum(list(map(lambda obj: obj.value, list(args)))) == 13:
                # compare to suits (hard mode)
                if self._level == 'hard':
                    if len(args) != 1:
                        assert reduce(
                            lambda a, b: a.suit == b.suit if a else None,
                            list(args)), 'different suits'

                for item in args:
                    self._del_card(item)
            else:
                raise ValueError('sum of values is not 13')
        else:
            raise ValueError('one of the cards is closed')

    @staticmethod
    def hint(current_add_card, open_cards):
        """Return cards which can be compare.
        :param current_add_card: active card from additional deck
        :param open_cards: all opened cards from pyramid
        """
        assert isinstance(current_add_card, Card), 'incorrect Card object'
        assert isinstance(open_cards, list), 'open_cards parameter ' \
                                             'must be in list type'




    @property
    def table(self):
        """Return TableCard object."""
        return self._table_obj

    @property
    def card_from_additional_deck(self):
        """Return card from additional deck."""
        deck_ = self._table_obj.additional_deck.deck
        if deck_:
            current_card = deck_.pop()
            if current_card.rank is not None:
                current_card.status = True
            self._card_stack.append(current_card)
            if not deck_:
                deck_.extend(self._card_stack)
                self._card_stack.clear()
            return current_card
        for card in self._card_stack:
            card.status = False

    @property
    def card_stack(self):
        """Return cards stack."""
        return self._card_stack

    @property
    def level(self):
        """Return game level."""
        return self._level

    @level.setter
    def level(self, level):
        """Set game level value."""
        levels = ['easy', 'hard']
        assert level in levels, 'incorrect level'
        self._level = level


#
# def test():
#     d = DeckGenerator()
#     # d.shuffle()
#     t = TableCard(d)
#     t.generate_pyramid()
#     for i in t.pyramid_deck:
#         for j in i:
#             j.status = True
#     print(t)
#     for i in t.additional_deck.deck:
#         i.status = True
#         print(t.additional_deck.deck.index(i), i)
#     gl = GameLogic(t)
#     gl.compare_card(t.pyramid_deck[-1][5])
#     gl.compare_card(t.additional_deck.deck[12])
#     print(t)
#     for i in t.additional_deck.deck:
#         i.status = True
#         print(t.additional_deck.deck.index(i), i)
#     # t = gl.redo_changes()
#     # print(gl.table.pyramid_deck[-1][5])
#     print(t)
#     for i in t.additional_deck.deck:
#         i.status = True
#         print(t.additional_deck.deck.index(i), i)
#
#
# if __name__ == '__main__':
#     test()
