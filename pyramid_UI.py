import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtCore import Qt, QPoint
from deck import Card
from deck import DeckGenerator
from table import TableCard
from logic import GameLogic
import background_rc


class Pyramid(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('pyramid.ui')
        self.ui.setWindowTitle('Pyramid Solitaire')
        self.ui.setWindowIcon(QIcon(os.path.join('images', 'main_window_icon.'
                                                           'png')))
        # -- Card size
        self.width = self.ui.label_00.width()  # 80 px
        self.height = self.ui.label_00.height()  # 116 px
        self.cards_labels = []  # all labels on form
        self.labels_coord = []
        self.selected_card = None  # current active card
        self.last_point = None  # coord of active card (for back to the
                                # start pos)
        self.b_move = False  # card move bool
        self.card_ = None  # Card object
        self.addCardLeft = self.ui.labelAddDeckLeft
        self.addCardRightF = self.ui.labelAddDeckRightF
        self.addCardRightB = self.ui.labelAddDeckRightB

        self.initUI()

    def initUI(self):
        # -- Global
        d = DeckGenerator()
        d.shuffle()
        self.deck = d.deck
        t = TableCard(d)
        t.generate_pyramid()
        gl = GameLogic(t)
        self.g_logic = gl
        self.table = self.g_logic.table
        self.pyramid_cards = self.table.pyramid_deck_linear

        # open bottom pyramid row
        for card in self.table.pyramid_deck[-1]:
            card.status = True
        # set pixmap for pyramid cards
        for row in range(len(self.table.pyramid_deck)):
            for card in range(len(self.table.pyramid_deck[row])):
                eval('self.ui.label_{}.setPixmap(self.table.pyramid_deck[row]'
                     '[card].pixmap)'.format(str(row) + str(card)))
                # add labels_ui
                self.cards_labels.append(eval('self.ui.label_{}'.format(
                    str(row) + str(card))))

        # for add cards
        self.addCardLeft.mousePressEvent = self.add_deck_clicked
        self.addCardRightF.mouseMoveEvent = self.mouseMoveEvent
        self.addCardRightF.mouseReleaseEvent = self.mouseReleaseEvent
        self.addCardLeft.setPixmap(
            QPixmap('images/back.png'))
        self.addCardRightF.setVisible(False)  # by default - hide
        self.addCardRightB.setPixmap(QPixmap('images/transparent_back.png'))
        # set event for all labels
        for lbl in self.cards_labels:
            lbl.mouseMoveEvent = self.mouseMoveEvent
            lbl.mouseReleaseEvent = self.mouseReleaseEvent
            self.labels_coord.append(lbl.pos())
        self.ui.mousePressEvent = self.mousePressEvent  # for all screen

        # -- actions
        new_game_action = self.ui.actionNew_Game
        new_game_action.triggered.connect(self.start_new_game)
        exit_action = self.ui.actionExit
        exit_action.triggered.connect(self.show_quit_message)
        cheat_action = self.ui.actionCheat
        cheat_action.triggered.connect(self.cheat)

        self.ui.show()

    def add_deck_clicked(self, *args):
        self.addCardRightF.setVisible(True)
        self.ui.statusbar.showMessage(str(len(self.g_logic.card_stack)))  # test
        add_card = self.g_logic.card_from_additional_deck
        while add_card.rank is None:
            add_card = self.g_logic.card_from_additional_deck
        self.addCardRightF.setPixmap(add_card.pixmap)
        if len(self.g_logic.card_stack) > 1:
            self.addCardRightB.setPixmap(self.g_logic.card_stack[-2].pixmap)
        if not self.g_logic.card_stack:
            self.addCardLeft.setPixmap(QPixmap('images/transparent_back.png'))
            self.addCardRightF.setPixmap(QPixmap('images/back.png'))
        else:
            self.addCardLeft.setPixmap(QPixmap('images/back.png'))

    def mousePressEvent(self, event):
        print('press')
        if event.x() in range(self.addCardRightF.x(), self.addCardRightF.x() + self.width) and \
                event.y() in range(self.addCardRightF.y(), self.addCardRightF.y() + self.height):
            # add card press
            print('stock')
            try:
                self.card_ = self.g_logic.card_stack[-1]
            except IndexError:
                pass
            self.selected_card = self.addCardRightF
            self.last_point = self.selected_card.pos()
            if event.button() == Qt.LeftButton:
                self.b_move = True
            return
        for c in self.labels_coord:  # c - coord (pos())
            self.card_ = self.pyramid_cards[self.labels_coord.index(c)]
            if event.x() in range(c.x(), c.x() + self.width) and event.y() in \
                    range(c.y(), c.y() + self.height):
                # test
                print('Current card: {}-{}, {}-{}'.format(str(c.x()), str(
                    c.x() + self.width), str(c.y()), str(c.y() + self.height)))
                if self.card_.status:
                    self.selected_card = self.cards_labels[
                        self.labels_coord.index(c)]
                    self.last_point = self.selected_card.pos()
                    if event.button() == Qt.LeftButton:
                        self.b_move = True
                    break

    def mouseMoveEvent(self, event):
        print('move')
        if (event.buttons() == Qt.LeftButton) and self.b_move and \
                self.card_.status:
            self.selected_card.move(self.selected_card.mapToParent(event.pos()))
            self.selected_card.raise_()

    def mouseReleaseEvent(self, event):
        print('release')
        self.b_move = False
        release_coord = self.selected_card.pos()
        release_card_x = release_coord.x()
        release_card_y = release_coord.y()
        if self.card_.status:
            try:
                if self.card_.value == 13:  # King
                    self.g_logic.compare_card(self.card_)
                    self.update_pyramid()
                for c in self.labels_coord:
                    if self.pyramid_cards[self.labels_coord.index(c)].status:
                        print('Card: x-{};y-{}'.format(str(c.x()), str(c.y())))
                        print('Coord x: {}-{}'.format(str(c.x()-self.width//2), str(c.x()+self.width//2)))
                        if release_card_x in range(c.x()-self.width//2,
                                                    c.x()+self.width//2) \
                            and release_card_y in range(c.y()-self.height//2, c.y()+self.height//2):
                            print('here')
                            self.g_logic.compare_card(self.card_, self.pyramid_cards[self.labels_coord.index(c)])
                self.update_pyramid()
            except ValueError:
                pass
            self.selected_card.move(self.last_point)

    def update_pyramid(self):
        for row in range(len(self.table.pyramid_deck) - 1, 0, -1):
            for item in range(1, row + 1):
                if self.table.pyramid_deck[row][item].rank is None and \
                   self.table.pyramid_deck[row][item - 1].rank is None and \
                   self.table.pyramid_deck[row - 1][item - 1].status is False and \
                   self.table.pyramid_deck[row - 1][item - 1].rank is not None:
                    self.table.pyramid_deck[row - 1][item - 1].status = True
        # update labels
        for row in range(len(self.table.pyramid_deck)):
            for card in range(len(self.table.pyramid_deck[row])):
                eval('self.ui.label_{}.setPixmap(self.table.pyramid_deck[row]'
                     '[card].pixmap)'.format(str(row) + str(card)))
        for c in self.pyramid_cards:  # check pyramid
            if c.rank is None:
                self.cards_labels[self.pyramid_cards.index(c)].setVisible(False)
        for c in self.g_logic.card_stack:
            if c.rank is None:
                self.addCardRightF.setVisible(False)
        if self.table.pyramid_deck[0][0].rank is None:
            self.show_game_over_message()

    # Slots for actions
    def start_new_game(self):
        """Start new game, with new objects."""
        for c in self.cards_labels:
            c.setVisible(True)
        self.initUI()

    def show_quit_message(self):
        reply = QMessageBox.question(self, 'Quit message', 'Are you sure you w'
                                                           'ant to exit?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.ui.close()

    def show_game_over_message(self):
        reply = QMessageBox.information(self, 'Game over', 'Congratulation!', QMessageBox.Ok, QMessageBox.Ok)
        self.start_new_game()

    def cheat(self):
        for row in self.table.pyramid_deck:
            for card in row:
                card.rank = None
        self.update_pyramid()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Pyramid()
    sys.exit(app.exec_())
