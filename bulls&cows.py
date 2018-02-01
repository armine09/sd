from PySide import QtCore, QtGui
import sys
from random import randint, choice
from copy import copy


class Bulls_and_cows_guess(QtCore.QObject):
    def __init__(self):
        self.__data = gen()
        self.count = 0
        self.prev = '0000'
        print(self.__data)

    def check(self):
        value = LineEdit.text()
        if value == self.__data:
            self.count += 1
            Label.setText('Congratulations')
            if self.count == 1:
                Label1.setText('You needed 1 attempt')
            else:
                Label1.setText('You needed ' + str(self.count) + ' attempts')
            text, ok = QtGui.QInputDialog.getText(GuessWindow, 'Input Dialog', 'Enter your name:')
            self.write_file(text)
            GiveinButton.hide()
            NewGameButton.show()
            CheckButton.setEnabled(False)
        elif right(value):
            res = result(self.__data, value)
            ans = answer(res[0], res[1])
            if self.prev != value:
                self.count += 1
            self.prev = value
            Label.setText('You have')
            Label1.setText(ans)
        else:
            ans = 'Not correct'
            self.prev = value
            Label.setText(ans)
            Label1.setText('')
        return

    def write_file(self, name):
        List = []
        try:
            f = open('Results.txt', 'r')
            s = f.readline()
            while s != '':
                l = s.split()
                a = int(l[-1])
                b = ' '.join(l[:-1])
                List += [[a, b]]
                s = f.readline()
            f.close()
        except FileNotFoundError:
            f = open('Results.txt', 'w')
            f.close()
        f = open('Results.txt', 'w')
        List += [[self.count, name]]
        List.sort()
        if len(List) > 7:
            List = List[:7]
        for i in List:
            f.write(i[1] + ' ' + str(i[0]))
            f.write('\n')
        f.close()

    def new(self):
        Label1.setText('The number was ' + self.__data)
        Label.setText('A new game has started')
        LineEdit.setText('')
        self.__data = gen()
        print(self.__data)
        self.prev = '0000'
        self.count = 0
        CheckButton.setEnabled(True)

    def anew(self):
        Label.setText('')
        Label1.setText('')
        self.__data = gen()
        print(self.__data)
        self.prev = '0000'
        self.count = 0
        CheckButton.setEnabled(True)
        GiveinButton.show()
        NewGameButton.hide()


class Bulls_and_cows_think(QtCore.QObject):
    def __init__(self):
        All = []
        self.__all = []
        for i in range(1023, 9877):
            if right(str(i)):
                self.__all += [i]
        self.__all = set(self.__all)
        self.ver = copy(self.__all)
        
    def check(self, b, c, num):
        List = list(self.ver)
        for i in List:
            if result(str(i), str(num)) != (b, c):
                self.ver.remove(i)
        if len(self.ver) == 0:
            self.ver = set(List)
            return False
        return True

    def play(self):
        global num
        Label5.setText('')
        b, c = LineEdit1.text(), LineEdit2.text()
        try:
            b = int(b)
            c = int(c)
        except:
            Label5.setText('Must be a number')
            return 
        if b + c > 4 or b < 0 or c < 0:
            Label5.setText('Provide the correct input, please')
            return
        elif b == 4 and c == 0:
            Label2.hide()
            LineEdit1.setText('')
            LineEdit2.setText('')
            Label5.setText('You can start a new game')
        else:
            a = self.check(b, c, num)
            if not a:
                Label5.setText('There were some mistakes in your input' + '\n' + 'You need to start a new game')
                OkButton.setEnabled(False)
                LineEdit1.setText('')
                LineEdit2.setText('')
                return
        num = choice(list(self.ver))
        Label2.setText('My number is ' + str(num))

    def anew(self):
        self.ver = copy(self.__all)
        Label5.setText('')
        Label2.show()
        LineEdit1.setText('')
        LineEdit2.setText('')
        OkButton.setEnabled(True)


def gen():
    s = str(randint(1023, 9876))
    while not right(s):
        s = str(randint(1023, 9876))
    return s


def right(s):
    if len(s) != 4:
        return False
    for i in s:
        if '0' > i or i > '9':
            return False
    if s[0] == '0':
        return False
    if len(set(list(s))) != 4:
        return False
    return True


def result(s, num):
    bulls, cows = 0, 0
    Set = set(list(s))
    num = str(num)
    s = str(s)
    for i in range(4):
        if s[i] == num[i]:
            bulls += 1
        elif num[i] in Set:
            cows += 1
    return bulls, cows


def answer(bulls, cows):
    ans = ''
    if bulls == 0:
        ans += 'no bulls and '
    elif bulls == 1:
        ans += '1 bull and '
    else:
        ans += str(bulls) + ' bulls and '    
    if cows == 0:
        ans += 'no cows'
    elif cows == 1:
        ans += '1 cow'
    else:
        ans += str(cows) + ' cows'
    return ans


def message():
    msgBox = QtGui.QMessageBox(Main)
    msgBox.setGeometry(200, 200, 200, 200)
    f = open('Results.txt', 'r')
    s = f.read()
    msgBox.setText(s)
    msgBox.exec_()
    f.close()


app = QtGui.QApplication(sys.argv)

Main = QtGui.QMainWindow()
Main.setWindowTitle("Menu")
Main.setGeometry(200, 200, 280, 250)

GuessButton = QtGui.QPushButton("Guess", Main)
GuessButton.setGeometry(40, 30, 200, 50)
ThinkButton = QtGui.QPushButton("Think", Main)
ThinkButton.setGeometry(40, 100, 200, 50)
ScoresButton = QtGui.QPushButton("Show best results", Main)
ScoresButton.setGeometry(40, 170, 200, 50)
try:
    f = open('Results.txt', 'r')
except FileNotFoundError:
    f = open('Results.txt', 'w')
f.close()

Game1 = Bulls_and_cows_guess()
Game2 = Bulls_and_cows_think()

GuessWindow = QtGui.QMainWindow(Main)
GuessWindow.setWindowTitle("Bulls and cows")
GuessWindow.resize(280, 160)
QtCore.QObject.connect(GuessButton, QtCore.SIGNAL("clicked()"), GuessWindow.show)

CheckButton = QtGui.QPushButton("Check", GuessWindow)
CheckButton.setGeometry(160, 15, 100, 50)
GiveinButton = QtGui.QPushButton("Give in", GuessWindow)
GiveinButton.setGeometry(160, 70, 100, 50)
NewGameButton = QtGui.QPushButton("New Game", GuessWindow)
NewGameButton.setGeometry(160, 70, 100, 50)
NewGameButton.hide()
LineEdit = QtGui.QLineEdit(GuessWindow)
LineEdit.setGeometry(20, 20, 100, 30)
Label = QtGui.QLabel(GuessWindow)
Label.setGeometry(20, 70, 150, 15)
Label1 = QtGui.QLabel(GuessWindow)
Label1.setGeometry(20, 90, 150, 15)

QtCore.QObject.connect(CheckButton, QtCore.SIGNAL("clicked()"), Game1.check)
QtCore.QObject.connect(GiveinButton, QtCore.SIGNAL("clicked()"), Game1.new)
QtCore.QObject.connect(NewGameButton, QtCore.SIGNAL("clicked()"), Game1.anew)
QtCore.QObject.connect(ScoresButton, QtCore.SIGNAL("clicked()"), message)


ThinkWindow = QtGui.QMainWindow(Main)
ThinkWindow.setWindowTitle("Bulls and cows")
ThinkWindow.resize(260, 200)
QtCore.QObject.connect(ThinkButton, QtCore.SIGNAL("clicked()"), ThinkWindow.show)

Label2 = QtGui.QLabel(ThinkWindow)
Label2.setGeometry(10, 10, 150, 15)        
Label3 = QtGui.QLabel(ThinkWindow)
Label3.setGeometry(10, 45, 40, 15)
Label3.setText('Bulls:')
LineEdit1 = QtGui.QLineEdit(ThinkWindow)
LineEdit1.setGeometry(55, 40, 50, 30)
Label4 = QtGui.QLabel(ThinkWindow)
Label4.setGeometry(10, 80, 40, 15)
Label4.setText('Cows:')
LineEdit2 = QtGui.QLineEdit(ThinkWindow)
LineEdit2.setGeometry(55, 80, 50, 30)
Label5 = QtGui.QLabel(ThinkWindow)
Label5.setGeometry(10, 130, 250, 30)
OkButton = QtGui.QPushButton("Enter", ThinkWindow)
OkButton.setGeometry(120, 30, 100, 40)
NewGameButton1 = QtGui.QPushButton("New Game", ThinkWindow)
NewGameButton1.setGeometry(120, 75, 100, 40)

num = choice(list(Game2.ver))
Label2.setText('My number is ' + str(num))
QtCore.QObject.connect(OkButton, QtCore.SIGNAL("clicked()"), Game2.play)
QtCore.QObject.connect(NewGameButton1, QtCore.SIGNAL("clicked()"), Game2.anew)


Main.show()
app.exec_()