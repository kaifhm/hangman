from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import random

chance_left = 10
hidden = ''
entered = ''
category = 'Animals and Birds'
word = ''


def get_word():
    global word
    with open(f"{category}.csv") as file:
        word_list = file.readlines()
    word = random.choice(word_list)[:-1].upper()
    return word


get_word()


def set_hidden():
    global hidden, entered
    hidden = ''.join(
        ['_' if i.isalpha() and i not in entered else i for i in word])
    return hidden


set_hidden()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(430, 126, 1058, 828)

        font = QtGui.QFont('Ubuntu Mono', 44)
        font.setLetterSpacing(0, 115)

        self.word = QtWidgets.QLabel(self)
        self.word.setGeometry(QtCore.QRect(200, 445, 691, 129))
        self.word.setAlignment(QtCore.Qt.AlignCenter)
        self.word.setWordWrap(True)
        self.word.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.word.setText(hidden)
        self.word.setFont(font)

        font = QtGui.QFont()
        font.setPointSize(18)

        self.top_names = list('QWERTYUIOP')
        self.mid_names = list('ASDFGHJKL')
        self.bottom_names = list('ZXCVBNM')

        self.top_buttons = [NewButton(self) for i in range(10)]
        for i in range(10):
            self.top_buttons[i].setGeometry(
                QtCore.QRect(200 + i*70, 610, 61, 51))
            self.top_buttons[i].setFont(font)
            self.top_buttons[i].clicked.connect(self.top_buttons[i].on_click)

        self.mid_buttons = [NewButton(self) for i in range(9)]
        for i in range(9):
            self.mid_buttons[i].setGeometry(
                QtCore.QRect(220 + i*70, 670, 61, 51))
            self.mid_buttons[i].setFont(font)
            self.mid_buttons[i].clicked.connect(self.mid_buttons[i].on_click)

        self.bottom_buttons = [NewButton(self) for i in range(7)]
        for i in range(len(self.bottom_buttons)):
            self.bottom_buttons[i].setGeometry(
                QtCore.QRect(260 + i*70, 730, 61, 51))
            self.bottom_buttons[i].setFont(font)
            self.bottom_buttons[i].clicked.connect(
                self.bottom_buttons[i].on_click)

        self.chance = QtWidgets.QLabel(self)
        self.chance.setGeometry(QtCore.QRect(10, 10, 256, 61))
        self.chance.setText(f'CHANCES LEFT: {chance_left}')
        self.chance.setFont(font)

        self.hang = QtWidgets.QLabel(self)
        canvas = QtGui.QPixmap(391, 381)
        canvas.fill(Qt.transparent)
        self.hang.setGeometry(QtCore.QRect(334, 20, 391, 381))
        self.hang.setPixmap(canvas)
        self.draw()

        self.dropdown = QtWidgets.QComboBox(self)
        self.dropdown.addItems(
            ['Animals and Birds', 'Cars', 'Vocabulary', 'Countries'])
        self.dropdown.setGeometry(820, 10, 231, 41)
        self.dropdown.currentIndexChanged.connect(self.change_subject)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setWindowTitle("Hangman")

    def retranslateUi(self):

        for i in range(10):
            v = self.top_buttons[i]
            v.setText(self.top_names[i])
            v.setEnabled(True)

        for i in range(9):
            v = self.mid_buttons[i]
            v.setText(self.mid_names[i])
            v.setEnabled(True)

        for i in range(7):
            v = self.bottom_buttons[i]
            v.setText(self.bottom_names[i])
            v.setEnabled(True)

    def change_subject(self):
        global category
        category = self.dropdown.currentText()
        self.set_category()
        self.play_again()

    def set_category(self):
        global category
        with open(f"{category}.csv") as file:
            word_list = file.readlines()
        word = random.choice(word_list)[:-1].upper()

    def update_word(self, letter):
        global chance_left
        new = ''
        # checker = ''
        for i in word:
            if i in entered or not i.isalpha():
                new += i
            else:
                new += '_'

        self.word.setText(new)

        if letter not in word:
            chance_left -= 1
            self.chance.setText(f'CHANCES LEFT: {chance_left}')
            self.chance.updateGeometry()
            self.draw()

        if new == word:
            self.show_dialog('Win!!', 'You Won!!', 0)

        if chance_left == 0:
            self.show_dialog('Lose!!', 'You Lost!!', 1)

    def draw(self):
        painter = QtGui.QPainter(self.hang.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(7)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        if chance_left == 10:
            painter.drawLine(0, 375, 180, 375)  # base
            painter.drawLine(90, 375, 90, 50)  # pole
            painter.drawLine(90, 50, 230, 50)  # hanger
            painter.drawLine(230, 50, 230, 90)  # hook
        elif chance_left == 9:
            radius = 80
            painter.drawEllipse(190, 90, radius, radius)  # head
            self.update()
        elif chance_left == 8:
            painter.drawLine(230, 170, 230, 250)  # trunk
            self.update()
        elif chance_left == 7:
            painter.drawLine(230, 250, 190, 320)  # leg.R
            self.update()
        elif chance_left == 6:
            painter.drawLine(230, 250, 270, 320)  # leg.L
            self.update()
        elif chance_left == 5:
            painter.drawLine(230, 170, 190, 240)  # hand.R
            self.update()
        elif chance_left == 4:
            painter.drawLine(230, 170, 270, 240)  # hand.L
            self.update()
        elif chance_left == 3:
            pen.setWidth(10)
            brush = QtGui.QBrush()
            brush.setStyle(Qt.SolidPattern)
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawEllipse(210, 115, 5, 5)  # eye.R
            self.update()
        elif chance_left == 2:
            pen.setWidth(10)
            painter.setPen(pen)
            brush = QtGui.QBrush()
            brush.setStyle(Qt.SolidPattern)
            painter.setBrush(brush)
            painter.drawEllipse(245, 115, 5, 5)  # eye.L
            pen.setWidth(7)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            self.update()
        elif chance_left == 1:
            painter.drawLine(230, 128, 230, 136)
            self.update()
        elif chance_left == 0:
            painter.drawArc(QtCore.QRect(210, 150, 40, 40), 700, 1440)
            self.update()
        painter.end()

    def show_dialog(self, title, message, ans):
        msg = QtWidgets.QMessageBox()

        s = 'Try' if ans else 'Play'

        r = msg.information(
            self, title, f"{message}\n\nThe word was {word}. {s} again?", msg.Yes | msg.No)
        if r == msg.Yes:
            self.play_again()
        else:
            sys.exit()

    def play_again(self):
        global entered, chance_left
        chance_left = 10
        self.chance.setText(f'CHANCES LEFT: {chance_left}')
        self.chance.updateGeometry()
        canvas = QtGui.QPixmap(391, 381)
        canvas.fill(Qt.transparent)
        self.hang.setPixmap(canvas)
        entered = ''
        self.retranslateUi()
        get_word()
        self.word.setText(set_hidden())
        self.draw()


class NewButton(QtWidgets.QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def on_click(self):
        global entered
        self.setEnabled(False)
        entered += self.text()
        ui.update_word(self.text())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()

    ui.show()

    sys.exit(app.exec_())
