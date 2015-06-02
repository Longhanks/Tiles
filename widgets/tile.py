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
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QPropertyAnimation, QRect, pyqtSignal


class Tile(QLabel):
    moved = pyqtSignal()

    def __init__(self, parent=None):
        super(Tile, self).__init__(parent)
        self.isEmpty = False
        self.perfectPos = None
        self.hasPerfectPos = True
        self.moveEnabled = False

    def mousePressEvent(self, event):
        if not self.moveEnabled:
            return
        if self.switch():
            self.moved.emit()

    def switch(self, anim=True):
        var = False
        for neighbor in self.getNeighbors():
            if neighbor.isEmpty:
                Xself = self.pos().x()
                Yself = self.pos().y()
                Xneigh = neighbor.pos().x()
                Yneigh = neighbor.pos().y()
                if self.perfectPos.x() == Xneigh and \
                   self.perfectPos.y() == Yneigh:
                    self.hasPerfectPos = True
                else:
                    self.hasPerfectPos = False
                if neighbor.perfectPos.x() == Xself and \
                   neighbor.perfectPos.y() == Yself:
                    neighbor.hasPerfectPos = True
                else:
                    neighbor.hasPerfectPos = False
                if anim:
                    self.animation = QPropertyAnimation(self, "geometry")
                    self.animation.setDuration(200)
                    self.animation.setEndValue(QRect(Xneigh,
                                                     Yneigh,
                                                     self.width(),
                                                     self.height()))
                    self.animation.start()
                else:
                    self.move(Xneigh, Yneigh)
                neighbor.move(Xself, Yself)
                var = True
        return var

    def getNeighbors(self):
        neighbors = []
        x = self.pos().x()
        y = self.pos().y()
        if self.parent().childAt(x-1, y):
            neighbors.append(self.parent().childAt(x-1, y))
        if self.parent().childAt(x+41, y):
            neighbors.append(self.parent().childAt(x+41, y))
        if self.parent().childAt(x, y-1):
            neighbors.append(self.parent().childAt(x, y-1))
        if self.parent().childAt(x, y+41):
            neighbors.append(self.parent().childAt(x, y+41))
        return neighbors
