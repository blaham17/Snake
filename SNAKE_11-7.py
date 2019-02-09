import sys, random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import *

n = 10
p = 30
pole = []

class Snake(QWidget):
    def __init__(self, snake_x, snake_y, current_state, next_state, n, p):
        super().__init__()
        self.snake_x = snake_x
        self.snake_y = snake_y
        self.snake_length = 2
        self.pole = pole
        self.pole[self.snake_y][self.snake_x] = 1
        self.n = n
        self.p = p
        self.food_x = random.randint(0, self.n -1)
        self.food_y = random.randint(0, self.n -1)
        while True:
            self.food_x = (random.randint(0, self.n - 1))
            self.food_y = (random.randint(0, self.n - 1))
            if self.pole[self.food_y][self.food_x] != 0:
                continue
            else:
                break
        self.pole[self.food_y][self.food_x] = -1
        self.current_state = current_state
        self.next_state = next_state
        self.rychlost = 200
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.HniSe)
        self.timer1.start(self.rychlost)
        self.skore = 0
        self.grid_x = 0
        self.grid_y = 0
        self.prohra = 0
        self.level = 1

    for i in range(0, n):
        pole.append(n*[0])

    def paintEvent(self, event):
        qp = QPainter(self)
        if self.prohra == 0:
            self.grid_y = 0
            for i in self.pole:
                self.grid_x = 0
                for j in i:
                    if j == 0:
                        pass
                    if j == -2:
                        qp.setBrush(QColor(0, 0, 0))
                        qp.drawRect(self.p * self.grid_x, self.p * self.grid_y, self.p, self.p)
                    if j == -1:
                        qp.setBrush(QColor(255, 0, 0))
                        qp.drawRect(self.p * self.grid_x, self.p * self.grid_y, self.p, self.p)
                    if j == 1:
                        qp.setBrush(QColor(0, 0, 255))
                        qp.drawRect(self.p*self.grid_x, self.p*self.grid_y, self.p, self.p)
                    if j > 1:
                        qp.setBrush(QColor(0, 200, 255))
                        qp.drawRect(self.p*self.grid_x, self.p*self.grid_y, self.p, self.p)
                    self.grid_x += 1
                self.grid_y += 1
            qp.drawText(5, (self.n*self.p + 15), "SKORE: " + str(self.skore))
        elif self.prohra == 1:
            self.timer1.stop()
            qp.setFont(QFont("Font", self.p*self.n/10))         #ZJISTIT DRUHY FONTU
            qp.drawText(event.rect(), Qt.AlignCenter, "KONEC HRY!\nSKORE: "+str(self.skore))

    def keyPressEvent(self, m):
        if m.key() == Qt.Key_D:
            self.next_state = "R"
        if m.key() == Qt.Key_A:
            self.next_state = "L"
        if m.key() == Qt.Key_W:
            self.next_state = "U"
        if m.key() == Qt.Key_S:
            self.next_state = "D"
        if m.key() == Qt.Key_Escape:
            self.close()
            app.close()

    def HniSe(self):
        self.current_state = self.next_state
        self.grid_y = 0
        for i in self.pole:
            self.grid_x = 0
            for j in i:
                if j >= 1:
                    self.pole[self.grid_y][self.grid_x] += 1
                if j > self.snake_length:
                    self.pole[self.grid_y][self.grid_x] = 0
                self.grid_x += 1
            self.grid_y += 1

        if self.current_state == "R":
            if self.snake_x == self.n-1 and self.current_state == "R":
                self.prohra = 1
                self.update()
            else:
                self.snake_x += 1
                if self.pole[self.snake_y][self.snake_x] > 1 or self.pole[self.snake_y][self.snake_x] == -2:
                    self.prohra = 1
                    self.update()
                else:
                    self.pole[self.snake_y][self.snake_x] = 1
                    self.update()
        if self.current_state == "L":
            if self.snake_x == 0 and self.current_state == "L":
                self.prohra = 1
                self.update()
            else:
                self.snake_x -= 1
                if self.pole[self.snake_y][self.snake_x] > 1 or self.pole[self.snake_y][self.snake_x] == -2:
                    self.prohra = 1
                    self.update()
                else:
                    self.pole[self.snake_y][self.snake_x] = 1
                    self.update()
        if self.current_state == "U":
            if self.snake_y == 0 and self.current_state == "U":
                self.prohra = 1
                self.update()
            else:
                self.snake_y -= 1
                if self.pole[self.snake_y][self.snake_x] > 1 or self.pole[self.snake_y][self.snake_x] == -2:
                    self.prohra = 1
                    self.update()
                else:
                    self.pole[self.snake_y][self.snake_x] = 1
                    self.update()
        if self.current_state == "D":
            if self.snake_y == self.n-1 and self.current_state == "D":
                self.prohra = 1
                self.update()
            else:
                self.snake_y += 1
                if self.pole[self.snake_y][self.snake_x] > 1 or self.pole[self.snake_y][self.snake_x] == -2:
                    self.prohra = 1
                    self.update()
                else:
                    self.pole[self.snake_y][self.snake_x] = 1
                    self.update()

        if self.snake_x == self.food_x and self.snake_y == self.food_y:

            if self.level == 5:
                self.n = 15
                self.pole = []
                for i in range(0, self.n):
                    self.pole.append(self.n*[0])
                self.pole[7][7] = -2
                self.pole[7][8] = -2
                self.pole[7][9] = -2
                self.pole[8][7] = -2
                self.pole[8][8] = -2
                self.pole[8][9] = -2
                self.pole[9][7] = -2
                self.pole[9][8] = -2
                self.pole[9][9] = -2
                mw.resize((self.n*self.p), (self.n*self.p + 20))
                while self.pole[self.food_y][self.food_x] != 0:
                    self.food_x = (random.randint(0, self.n - 1))
                    self.food_y = (random.randint(0, self.n - 1))
                    continue
                self.rychlost = 300
                self.update()

            while self.pole[self.food_y][self.food_x] != 0:
                self.food_x = (random.randint(0, self.n -1))
                self.food_y = (random.randint(0, self.n -1))
                continue
            self.pole[self.food_y][self.food_x] = -1
            self.rychlost -= (0.05 * self.rychlost)
            self.timer1.stop()
            self.timer1 = QTimer()
            self.timer1.timeout.connect(self.HniSe)
            self.timer1.start(self.rychlost)
            self.skore += 10
            self.snake_length += 1
            self.level += 1
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = Snake(1, 1, "R", "R", n, p)
    mw.setWindowTitle('Snake')
    mw.resize((n*p), (n*p + 20))
    mw.show()
    sys.exit(app.exec_())
