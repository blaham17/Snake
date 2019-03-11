import sys, random
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import *

n = 10
p = 40

class Snake(QWidget):
    def __init__(self, n, p):
        super().__init__()
        self.Setup(n, p)

    def Setup(self, n, p):
        self.snake_x = 4
        self.snake_y = 4
        self.level = 0
        self.snake_length = self.level + 2
        self.mapa_0()
        self.pole[self.snake_y][self.snake_x] = 1
        self.n = n
        self.p = p
        self.Jidlo()
        self.current_state = "R"
        self.next_state = "R"
        self.rychlost = 200
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.HniSe)
        self.timer1.start(self.rychlost)
        self.skore = 0
        self.bonus = 0
        self.grid_x = 0
        self.grid_y = 0
        self.prohra = 0
        self.koeficient_rychlosti = 0.1
    def center_the_screen(self):
        AG = QDesktopWidget().availableGeometry()
        okno = self.geometry()
        okno_x = (AG.width() - okno.width())/2
        okno_y = (AG.height() - okno.height())/2
        self.move(okno_x, okno_y)

    def Jidlo(self):
        self.food_x = random.randint(0, self.n - 1)
        self.food_y = random.randint(0, self.n - 1)
        while self.pole[self.food_y][self.food_x] != 0:
            self.food_x = (random.randint(0, self.n - 1))
            self.food_y = (random.randint(0, self.n - 1))
            continue
        self.pole[self.food_y][self.food_x] = -1

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.prohra == 0:
            self.grid_y = 0
            for i in self.pole:
                self.grid_x = 0
                for j in i:
                    if j == -2:
                        painter.setBrush(QColor(0, 0, 0))
                        painter.drawRect(self.p * self.grid_x, self.p * self.grid_y, self.p, self.p)
                    if j == -1:
                        painter.setBrush(QColor(255, 0, 0))
                        painter.drawRect(self.p * self.grid_x, self.p * self.grid_y, self.p, self.p)
                    if j == 1:
                        painter.setBrush(QColor(0, 0, 255))
                        painter.drawRect(self.p*self.grid_x, self.p*self.grid_y, self.p, self.p)
                    if j > 1:
                        painter.setBrush(QColor(0, 200, 255))
                        painter.drawRect(self.p*self.grid_x, self.p*self.grid_y, self.p, self.p)
                    self.grid_x += 1
                self.grid_y += 1
            painter.drawText(5, (self.n*self.p + 15), "SKORE: " + str(self.skore) + "           LEVEL: " + str(self.level))
        elif self.prohra == 1:
            self.timer1.stop()
            painter.setFont(QFont("Default", self.p*self.n/10))
            painter.drawText(event.rect(), Qt.AlignCenter, "KONEC HRY!\nSKORE: "+str(self.skore))
            painter.setFont(QFont("Default", self.p*self.n/20))
            painter.drawText(event.rect(), Qt.AlignBottom, "Hrat znovu? [J]o/[N]e")

    def keyPressEvent(self, m):
        if self.prohra == 0:
            if m.key() == Qt.Key_D or m.key() == Qt.Key_Right:
                self.next_state = "R"
            if m.key() == Qt.Key_A or m.key() == Qt.Key_Left:
                self.next_state = "L"
            if m.key() == Qt.Key_W or m.key() == Qt.Key_Up:
                self.next_state = "U"
            if m.key() == Qt.Key_S or m.key() == Qt.Key_Down:
                self.next_state = "D"
        if self.prohra == 1:
            if m.key() == Qt.Key_J:
                self.Setup(n, p)
                okno.resize((self.n * self.p), (self.n * self.p + 20))
                okno.center_the_screen()
            if m.key() == Qt.Key_N:
                self.close()
                app.close()
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
            if self.snake_x == self.n - 1 or self.pole[self.snake_y][self.snake_x + 1] > 1 or self.pole[self.snake_y][self.snake_x + 1] == -2:
                self.prohra = 1
            else:
                self.snake_x += 1
                self.pole[self.snake_y][self.snake_x] = 1
            self.update()
        if self.current_state == "L":
            if self.snake_x == 0 or self.pole[self.snake_y][self.snake_x - 1] > 1 or self.pole[self.snake_y][self.snake_x - 1] == -2:
                self.prohra = 1
            else:
                self.snake_x -= 1
                self.pole[self.snake_y][self.snake_x] = 1
            self.update()
        if self.current_state == "U":
            if self.snake_y == 0 or self.pole[self.snake_y - 1][self.snake_x] > 1 or self.pole[self.snake_y - 1][self.snake_x] == -2:
                self.prohra = 1
            else:
                self.snake_y -= 1
                self.pole[self.snake_y][self.snake_x] = 1
            self.update()
        if self.current_state == "D":
            if self.snake_y == self.n-1 or self.pole[self.snake_y + 1][self.snake_x] > 1 or self.pole[self.snake_y + 1][self.snake_x] == -2:
                self.prohra = 1
            else:
                self.snake_y += 1
                self.pole[self.snake_y][self.snake_x] = 1
            self.update()
        if self.snake_x == self.food_x and self.snake_y == self.food_y:
            self.timer1.stop()
            self.level += 1
            self.snake_length += 1
            self.skore += 10 + self.bonus
            self.rychlost -= (self.koeficient_rychlosti * self.rychlost)
            if self.level == 5:
                self.mapa_5()
                self.bonus = self.level
            if self.level == 10:
                self.mapa_10()
                self.bonus = self.level
            if self.level == 15:
                self.mapa_15()
                self.bonus = self.level
            if self.level == 20:
                self.mapa_20()
                self.bonus = self.level
            if self.level == 25:
                self.mapa_25()
                self.bonus = self.level
            if self.level == 30:
                self.mapa_30()
                self.bonus = self.level
            if self.level == 35:
                self.mapa_35()
                self.bonus = self.level
            okno.resize((self.n * self.p), (self.n * self.p + 20))
            okno.center_the_screen()
            if self.level % 5 == 0 and self.level < 36:
                    self.next_state = "R"
            self.Jidlo()
            self.timer1 = QTimer()
            self.timer1.timeout.connect(self.HniSe)
            self.timer1.start(self.rychlost)

    def mapa_0(self):
        self.pole = []
        for i in range(0, n):
            self.pole.append(n * [0])
        self.snake_x = 4
        self.snake_y = 4
    def mapa_5(self):
        self.n = 15
        self.pole = []
        for i in range(0, self.n):
            self.pole.append(self.n * [0])
        for i in range(5, 10):
            for  j in range(5, 10):
                self.pole[i][j] = -2
        self.snake_x = 3
        self.snake_y = 3
        self.rychlost = 200
    def mapa_10(self):
        self.n = 15
        self.pole = []
        for i in range(0, self.n):
            self.pole.append(self.n * [0])
        for i in range(4, 11):
            self.pole[2][i] = -2
        for i in range (4, 11):
            self.pole[12][i] = -2
        for i in range(4,11):
            self.pole[i][2] = -2
        for i in range(4,11):
            self.pole[i][12] = -2
        self.pole[7][7] = -2
        self.snake_x = 5
        self.snake_y = 5
        self.rychlost = 220
    def mapa_15(self):
        self.n = 15
        self.pole = []
        for i in range(0, self.n):
            self.pole.append(self.n * [0])
        for i in (2, 5):
            for j in range(2, 6):
                self.pole[i][j] = -2
        for i in (9, 12):
            for j in range(9, 13):
                self.pole[i][j] = -2
        for i in (2, 5):
            for j in range(9, 13):
                self.pole[j][i] = -2
        for i in(9, 12):
            for j in range(2, 6):
                self.pole[j][i] = -2
        self.snake_x = 7
        self.snake_y = 7
        self.rychlost = 220
    def mapa_20(self):
        self.n = 15
        self.pole = []
        for i in range(0, self.n):
            self.pole.append(self.n * [0])
        for i in range (1, 14, 2):
            for j in range(1, 14, 2):
                self.pole[i][j] = -2
        self.snake_x = 6
        self.snake_y = 6
        self.rychlost = 240
    def mapa_25(self):
        self.n = 20
        self.pole = []
        for i in range(0, self.n):
            self.pole.append(self.n * [0])
        for i in (1, 2, 5, 6, 7, 8, 9):
            self.pole[1][i] = -2
        for i in (1, 2, 12, 13, 14, 15):
            self.pole [2][i] = -2
        for i in (4, 5, 9, 10):
            self.pole [4][i] = -2
        for i in (4, 10, 12):
            self.pole[5][i] = -2
        for i in (4, 10):
            self.pole[9][i] = -2
        for i in (4, 5, 9, 10):
            self.pole[10][i] = -2
        self.pole[12][5] = -2
        for i in range(5, 10):
            self.pole[i][1] = -2
        for i in range(12, 16):
            self.pole[i][2] = -2
        for i in range (3, 6):
            self.pole[15][i] = -2
        for i in (12, 13, 16, 18):
            self.pole[16][i] = -2
        for i in range(0, 12):
            self.pole[17][i] = -2
        for i in range(8, 13):
            self.pole[13][i] = -2
        for i in range(8, 13):
            self.pole[i][13] = -2
        for i in range(3, 6):
            self.pole[i][15] = -2
        for i in range(0, 12):
            self.pole[i][17] = -2
        for i in (12, 13, 18):
            self.pole[i][16] = -2
        self.pole[18][18] = -2
        self.pole[14][14] = -2
        self.snake_x = 7
        self.snake_y = 7
        self.rychlost = 250
    def mapa_30(self):
        self.n = 19
        self.pole = []
        for i in range(0, self.n):
            self.pole.append(self.n * [0])
        for i in (7, 8, 10, 11):
            for j in (7, 8, 10, 11):
                self.pole[j][i] = -2
        for i in (2, 3, 4, 5, 6, 12, 13, 14, 15, 16):
            for j in (2, 3, 4, 5, 6, 12, 13, 14, 15, 16):
                self.pole[j][i] = -2
        self.snake_x = 9
        self.snake_y = 9
        self.rychlost = 220
    def mapa_35(self):
        self.n = 23
        self.pole = []
        for i in range(0, self.n):
            self.pole.append(self.n * [0])
        for i in range(10, 13):
            for j in range(10, 13):
                self.pole[j][i] = -2
        for i in (3, 4, 5, 6, 16, 17, 18, 19):
            for j in (3, 4, 5, 6, 16, 17, 18, 19):
                self.pole[j][i] = -2
        self.snake_x = 8
        self.snake_y = 8
        self.koeficient_rychlosti = 0.05
        self.rychlost = 230
if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = Snake(n, p)
    okno.resize((n * p), (n * p + 20))
    okno.center_the_screen()
    okno.setWindowTitle("Snake")
    okno.show()
sys.exit(app.exec_())