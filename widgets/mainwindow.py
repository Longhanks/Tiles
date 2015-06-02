# Tile. Created on 28.05.2015
# Copyright (c) 2015 Andreas Schulz
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import random
import threading
import time

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QCoreApplication

from utilities import getResourcesPath
from widgets.tile import Tile


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi(os.path.join(getResourcesPath(), 'ui', 'mainwindow.ui'),
                   self)
        self.actionLoadPicture.triggered.connect(self.loadFile)
        self.actionShuffle.triggered.connect(self.shuffle)
        self.actionExit.triggered.connect(QCoreApplication.instance().quit)
        self.labels = self.findChildren(Tile)
        # counter for how many moves have been done.
        self.moves = 0
        # counter for how many seconds have passed.
        self.time = 0
        # thread which will update the label of passed time.
        self.timer = None
        # initial position of the labels is their perfect position.
        for label in self.labels:
            label.perfectPos = label.pos()
            label.moved.connect(self.successfulMove)

    def shuffle(self):
        self.stop = True
        if self.timer:
            self.timer.join()
            self.timer = None
        # re-init game
        self.setupGame(self.pic)

    def setupGame(self, pic):
        # reset time and restart timer
        self.stop = False
        self.time = 0
        self.timer = updateTimeThread(self)
        self.timer.daemon = True
        self.timer.start()

        # reset moves and label of moves
        self.moves = 0
        self.labelMoves.setText(str(self.moves))

        # transform the user's picture to a pixmap
        pixmap = QPixmap(pic)
        # scale the pixmap to fit the 160x160 game widget
        pixmap = pixmap.scaled(160, 160,
                               Qt.KeepAspectRatioByExpanding,
                               Qt.SmoothTransformation)

        # split pixmap and assign splitted pixmaps to tiles
        for label in self.labels:
            label.setPixmap(pixmap.copy(label.pos().x(),
                                        label.pos().y(),
                                        40,
                                        40))

        # top-left tile is empty.
        self.labels[0].isEmpty = True
        self.labels[0].setPixmap(QPixmap())

        # allow moving of tiles
        self.setMoveEnabled(True)

        # randomize position of tiles by switching them (animations turned off)
        for i in range(200):
            index = random.choice(range(16))
            self.labels[index].switch(False)

    def setMoveEnabled(self, bool):
        # parameter bool (dis-)allows moving of tiles.
        for label in self.labels:
            label.moveEnabled = bool

    def loadFile(self):
        # ask user for input of png, jpg or jpeg file.
        pic = QFileDialog.getOpenFileName(
            self,
            'Open picture',
            os.path.expanduser("~"),
            'Pictures (*.png *.jpg *.jpeg)')
        # if user entered valid picture, start the game.
        if pic[0]:
            self.pic = pic[0]
            self.setupGame(self.pic)

    def checkIfWon(self):
        # checks all tiles wether they are at the right position.
        win = True
        for label in self.labels:
            if not label.hasPerfectPos:
                # found at least one tile at wrong position.
                win = False
        if win:
            # stop timer thread and display victory message.
            self.stop = True
            self.timer.join()
            self.timer = None
            QMessageBox.information(self,
                                    "Victory!",
                                    "You won! You took " + str(self.moves) +
                                    " moves and " + str(self.time) +
                                    " seconds.")
            # disallow moving. If user wants to play again, use shuffle.
            self.setMoveEnabled(False)

    def successfulMove(self):
        # a tile was moved. Update moves label and then check if user won.
        self.moves += 1
        self.labelMoves.setText(str(self.moves))
        self.checkIfWon()


class updateTimeThread(threading.Thread):
    def __init__(self, mainwindowPointer):
        super(updateTimeThread, self).__init__()
        self.mw = mainwindowPointer

    def run(self):
        while not self.mw.stop:
            self.mw.time += 1
            self.mw.labelTime.setText(str(self.mw.time))
            time.sleep(1.0)
