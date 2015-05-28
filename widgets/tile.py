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

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor, QPixmap


class Tile(QLabel):
    def __init__(self, parent=None):
        super(Tile, self).__init__(parent)
        self.isEmpty = False
        self.neighbors = []
        self.currentPixmapName = None
        self.mw = self.parent().parent()

    def mousePressEvent(self, event):
        if self.parent().parent().pixmaps is None:
            return
        if self.switch():
            self.mw.moves += 1
            self.mw.labelMoves.setText(str(self.mw.moves))
            self.mw.checkIfWon()

    def switch(self):
        var = False
        for neighbor in self.neighbors:
            if neighbor.isEmpty:
                neighbor.setPixmap(QPixmap(self.pixmap()))
                empty = QPixmap(40, 40)
                empty.fill(QColor("white"))
                self.setPixmap(empty)
                neighbor.isEmpty = False
                self.isEmpty = True
                neighbor.currentPixmapName, self.\
                    currentPixmapName = self.\
                    currentPixmapName, neighbor.currentPixmapName
                var = True
        return var

    def checkIfPixmapFits(self):
        if self.isEmpty:
            return True
        elif self.currentPixmapName[6:] == self.objectName()[5:]:
            return True
        else:
            return False
