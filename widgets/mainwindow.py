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
from PyQt5.QtGui import QColor, QPixmap
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
        self.pixmaps = None
        self.moves = 0
        self.time = 0
        self.timer = None

        for label in self.labels:
            digits = [int(label.objectName()[5:-1]),
                      int(label.objectName()[6:])]

            upDigits = [digits[0], digits[1] - 1]
            downDigits = [digits[0], digits[1] + 1]
            leftDigits = [digits[0] - 1, digits[1]]
            rightDigits = [digits[0] + 1, digits[1]]

            neighboursDigits = [upDigits, downDigits, leftDigits, rightDigits]
            for neighboursDigit in neighboursDigits:
                digStr = ""
                for digit in neighboursDigit:
                    digStr += str(digit)
                digStr = "label" + digStr
                child = self.findChildren(Tile, digStr)
                if child:
                    label.neighbors.append(child[0])

    def splitPix(self, pixmap):
        pixmap00 = pixmap.copy(0, 0, 40, 40)
        pixmap10 = pixmap.copy(40, 0, 40, 40)
        pixmap20 = pixmap.copy(80, 0, 40, 40)
        pixmap30 = pixmap.copy(120, 0, 40, 40)
        pixmap01 = pixmap.copy(0, 40, 40, 40)
        pixmap11 = pixmap.copy(40, 40, 40, 40)
        pixmap21 = pixmap.copy(80, 40, 40, 40)
        pixmap31 = pixmap.copy(120, 40, 40, 40)
        pixmap02 = pixmap.copy(0, 80, 40, 40)
        pixmap12 = pixmap.copy(40, 80, 40, 40)
        pixmap22 = pixmap.copy(80, 80, 40, 40)
        pixmap32 = pixmap.copy(120, 80, 40, 40)
        pixmap03 = pixmap.copy(0, 120, 40, 40)
        pixmap13 = pixmap.copy(40, 120, 40, 40)
        pixmap23 = pixmap.copy(80, 120, 40, 40)
        pixmap33 = pixmap.copy(120, 120, 40, 40)
        pixmaps = [("pixmap00", pixmap00), ("pixmap10", pixmap10),
                   ("pixmap20", pixmap20), ("pixmap30", pixmap30),
                   ("pixmap01", pixmap01), ("pixmap11", pixmap11),
                   ("pixmap21", pixmap21), ("pixmap31", pixmap31),
                   ("pixmap02", pixmap02), ("pixmap12", pixmap12),
                   ("pixmap22", pixmap22), ("pixmap32", pixmap32),
                   ("pixmap03", pixmap03), ("pixmap13", pixmap13),
                   ("pixmap23", pixmap23), ("pixmap33", pixmap33)]
        return pixmaps

    def shuffle(self):
        self.stop = True
        if self.timer:
            self.timer.join()
            self.timer = None
        self.setupGame(self.pic)

    def setupGame(self, pic):
        self.stop = False
        self.time = 0
        self.timer = updateTimeThread(self)
        self.timer.daemon = True
        self.timer.start()

        self.moves = 0
        self.labelMoves.setText(str(self.moves))

        pixmap = QPixmap(pic)
        pixmap = pixmap.scaled(160, 160)
        self.pixmaps = self.splitPix(pixmap)

        indices = list(range(len(self.pixmaps)))
        labelIndex = 0
        for index in indices:
            self.labels[labelIndex].isEmpty = False
            self.labels[labelIndex].setPixmap(self.pixmaps[index][1])
            self.labels[labelIndex].currentPixmapName = self.pixmaps[index][0]
            labelIndex += 1

        pixmap = QPixmap(40, 40)
        pixmap.fill(QColor("white"))
        self.labels[0].isEmpty = True
        self.labels[0].setPixmap(pixmap)

        for i in range(200):
            index = random.choice(range(16))
            self.labels[index].switch()

    def loadFile(self):
        pic = QFileDialog.getOpenFileName(
            self,
            'Open picture',
            os.path.expanduser("~"),
            'Pictures (*.png *.jpg *.jpeg)')
        if pic[0]:
            self.pic = pic[0]
            self.setupGame(self.pic)

    def checkIfWon(self):
        win = True
        for label in self.labels:
            if label.checkIfPixmapFits():
                pass
            else:
                win = False
        if win:
            self.stop = True
            self.timer.join()
            self.timer = None
            QMessageBox.information(self,
                                    "Victory!",
                                    "You won! You took " + str(self.moves) +
                                    " moves and " + str(self.time) +
                                    " seconds.")
            self.pixmaps = None


class updateTimeThread(threading.Thread):
    def __init__(self, mainwindowPointer):
        super(updateTimeThread, self).__init__()
        self.mw = mainwindowPointer

    def run(self):
        while not self.mw.stop:
            self.mw.time += 1
            self.mw.labelTime.setText(str(self.mw.time))
            time.sleep(1.0)
