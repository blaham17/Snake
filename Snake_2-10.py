import sys, random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import *

n = 10                      #pocet policek v radku/sloupci
p = 30                      #velikost policka


class Snake(QWidget):
    def __init__(self, snake_x, snake_y, current_state, next_state, n, p):
        super().__init__()
        self.Setup(snake_x, snake_y, current_state, next_state, n, p)

    def Setup(self, snake_x, snake_y, current_state, next_state, n, p):
        self.snake_x = snake_x
        self.snake_y = snake_y
        self.snake_length = 6
        self.pole = []
        self.mapa_1()
        self.pole[self.snake_y][self.snake_x] = 1  # nastaveni souradnic hlavy
        self.n = n
        self.p = p
        self.Jidlo()
        self.current_state = current_state
        self.next_state = next_state
        self.rychlost = 200  # Rychlost
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.HniSe)
        self.timer1.start(self.rychlost)  # zacatek herniho cyklu??
        self.skore = 0
        self.grid_x = 0
        self.grid_y = 0
        self.prohra = 0
        self.level = 4

    def Jidlo(self):
        self.food_x = random.randint(0, self.n - 1)
        self.food_y = random.randint(0, self.n - 1)
        while self.pole[self.food_y][self.food_x] != 0:  # vygenerovani souradnic jidla
            self.food_x = (random.randint(0, self.n - 1))
            self.food_y = (random.randint(0, self.n - 1))
            continue
        self.pole[self.food_y][self.food_x] = -1

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
                        qp.setBrush(QColor(0, 0, 0))        #vykresleni prekazky
                        qp.drawRect(self.p * self.grid_x, self.p * self.grid_y, self.p, self.p)
                    if j == -1:
                        qp.setBrush(QColor(255, 0, 0))      #vykresleni jidla
                        qp.drawRect(self.p * self.grid_x, self.p * self.grid_y, self.p, self.p)
                    if j == 1:
                        qp.setBrush(QColor(0, 0, 255))      #vykresleni hlavy
                        qp.drawRect(self.p*self.grid_x, self.p*self.grid_y, self.p, self.p)
                    if j > 1:
                        qp.setBrush(QColor(0, 200, 255))    #vykresleni tela
                        qp.drawRect(self.p*self.grid_x, self.p*self.grid_y, self.p, self.p)
                    self.grid_x += 1
                self.grid_y += 1
            qp.drawText(5, (self.n*self.p + 15), "SKORE: " + str(self.skore))   #Skore v dolni casti hraci plochy
        elif self.prohra == 1:
            self.timer1.stop()                                                  #konec hry
            qp.setFont(QFont("Font", self.p*self.n/10))         #ZJISTIT DRUHY FONTU
            qp.drawText(event.rect(), Qt.AlignCenter, "KONEC HRY!\nSKORE: "+str(self.skore))
            qp.setFont(QFont("Font", self.p * self.n / 20))
            qp.drawText(event.rect(), Qt.AlignBottom, "Hrat znovu? [J]o/[N]e")

    def keyPressEvent(self, m):             #detekce klaves
        if self.prohra == 0:
            if m.key() == Qt.Key_D:
                self.next_state = "R"
            if m.key() == Qt.Key_A:
                self.next_state = "L"
            if m.key() == Qt.Key_W:
                self.next_state = "U"
            if m.key() == Qt.Key_S:
                self.next_state = "D"
        if self.prohra == 1:
            if m.key() == Qt.Key_J:                                     #RESTART
                self.Setup(1, 1, "R", "R", n, p)
                #self.__init__(1, 1, "R", "R", n, p)
                mw.resize((self.n * self.p), (self.n * self.p + 20))
            if m.key() == Qt.Key_N:
                self.close()
                app.close()
        if m.key() == Qt.Key_Escape:
            self.close()
            app.close()

    def HniSe(self):                                #HERNI CYKLUS
        self.current_state = self.next_state
        self.grid_y = 0
        for i in self.pole:
            self.grid_x = 0
            for j in i:
                if j >= 1:                          #ke kazdemu clanku hada se pricte jedna
                    self.pole[self.grid_y][self.grid_x] += 1
                if j > self.snake_length:
                    self.pole[self.grid_y][self.grid_x] = 0     #umaze se posledni clanek
                self.grid_x += 1
            self.grid_y += 1
                                        #POHYB HLAVY - pri narazu se hra ukonci, jinak hra pokracuje
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

        if self.snake_x == self.food_x and self.snake_y == self.food_y:     #Kdyz bylo snezeno jidlo:
            self.level += 1                                     #zvyseni levelu
            if self.level == 5:
                self.mapa_5()
            if self.level == 10:
                self.mapa_10()
            if self.level == 15:
                self.mapa_15()
            if self.level == 20:
                self.mapa_20()
            self.Jidlo()
            self.rychlost -= (0.05 * self.rychlost)             #zvyseni rychlosti
            self.timer1.stop()
            self.timer1 = QTimer()
            self.timer1.timeout.connect(self.HniSe)
            self.timer1.start(self.rychlost)
            self.skore += 10                                    #pricteni skore
            self.snake_length += 1                              #prodlouzeni hada
            self.update()

    def mapa_1(self):
        for i in range(0, n):  # vygenerovani pole
            self.pole.append(n * [0])
    def mapa_5(self):
        self.n = 15
        self.pole = []
        for i in range(0, self.n):          # vygenerovani noveho hraciho pole
            self.pole.append(self.n * [0])
        for i in (7, 8, 9):
            for j in (7,8, 9):
                self.pole[i][j] = -2
        mw.resize((self.n * self.p), (self.n * self.p + 20))
        self.snake_x = 1
        self.snake_y = 1
        self.next_state = "R"
        self.rychlost = 250
        self.update()
    def mapa_10(self):
        self.n = 15
        self.pole = []
        for i in range(0, self.n):  # vygenerovani noveho hraciho pole
            self.pole.append(self.n * [0])
        for i in range(4, 11):
            self.pole[2][i] = -2  # nastaveni prekazek
        for i in range (4, 11):
            self.pole[12][i] = -2
        for i in range(4,11):
            self.pole[i][2] = -2
        for i in range(4,11):
            self.pole[i][12] = -2
        self.pole[7][7] = -2
        #mw.resize((self.n * self.p), (self.n * self.p + 20))
        self.snake_x = 1
        self.snake_y = 1
        self.next_state = "R"
        self.rychlost = 250
        self.update()
    def mapa_15(self):
        self.n = 15
        self.pole = []
        for i in range(0, self.n):  # vygenerovani noveho hraciho pole
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
        #mw.resize((self.n * self.p), (self.n * self.p + 20))
        self.snake_x = 1
        self.snake_y = 1
        self.next_state = "R"
        self.rychlost = 250
        self.update()
    def mapa_20(self):
        self.n = 15
        self.pole = []
        for i in range(0, self.n):  # vygenerovani noveho hraciho pole
            self.pole.append(self.n * [0])
        for i in range (1, 14, 2):
            for j in range(1, 14, 2):
                self.pole[i][j] = -2
        #mw.resize((self.n * self.p), (self.n * self.p + 20))
        self.snake_x = 2
        self.snake_y = 2
        self.next_state = "R"
        self.rychlost = 250
        self.update()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = Snake(1, 1, "R", "R", n, p)
    mw.setWindowTitle('Snake')
    mw.resize((n*p), (n*p + 20))
    mw.show()
sys.exit(app.exec_())
