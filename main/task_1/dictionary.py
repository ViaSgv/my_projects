from PySide6.QtWidgets import (
    # Служебные
    QApplication,
    QMainWindow,
    QWidget,

    # Функциональные элементы
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QListWidget,

    # Организующие элементы
    QVBoxLayout,
    QHBoxLayout
    
)

from peewee import *
import os
import sys
import random

filename = 'words.db'
db = SqliteDatabase(filename)


class BaseModel(Model):
    class Meta:
        database = db


class Words(BaseModel):
    id = PrimaryKeyField(primary_key = True)
    word = CharField(max_length=100)
    desc = TextField()
    category = CharField(max_length=100)
    class Meta:
        table_name = 'word_list'


if os.path.exists(filename):
    pass
else:
    db.create_tables([Words])




class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        first_view = self.renderAdd()
        self.current_question = None
        self.true_ans = None


        # Итоговая компановка и вывод
        widget = QWidget()
        widget.setLayout(first_view)
        self.setCentralWidget(widget)

    def setNewView(self, view):
        widget = QWidget()
        widget.setLayout(view)
        self.setCentralWidget(widget)
    
    def renderRep(self):
        # Создаем элементы
        self.lb1 = QLabel('Слово')
        
        self.get_word_res = self.get_word()
        self.current_question = self.get_word_res[0]
        self.true_ans = self.get_word_res[1]


        self.lb2 = QLabel(self.current_question)
        self.lb4 = QLabel('Итог')
        self.lb5 = QLabel('')

        self.input1 = QLineEdit()

        self.btn1 = QPushButton('Проверить')
        self.btn2 = QPushButton('Добавление слов')
        self.btn3 = QPushButton('Следующее слово')

        self.btn1.clicked.connect(self.check_answer)
        self.btn2.clicked.connect(self.changeToAdd)
        self.btn3.clicked.connect(self.changeToRep)

        self.vlo1 = QVBoxLayout()
        self.vlo2 = QVBoxLayout()
        self.vlo3 = QVBoxLayout()

        self.vlo_enter = QVBoxLayout()
        self.main_layout = QVBoxLayout()

        # Заполняем блоки элементами
        self.vlo1.addWidget(self.lb1)
        self.vlo1.addWidget(self.lb2)

        self.vlo2.addWidget(self.lb3)
        self.vlo2.addWidget(self.input1)
        self.vlo2.addWidget(self.btn1)

        self.vlo3.addWidget(self.lb4)
        self.vlo3.addWidget(self.lb5)
        self.vlo3.addWidget(self.btn2)
        self.vlo3.addWidget(self.btn3)

        self.vlo_enter.addLayout(self.vlo1)
        self.vlo_enter.addLayout(self.vlo2)
        self.vlo_enter.addLayout(self.vlo3)
        self.main_layout.addLayout(self.vlo_enter)


        res_View = self.main_layout
        return res_View


    def renderAdd(self):
        # Создаем элементы
        self.lb1 = QLabel('Введите слово')
        self.lb2 = QLabel('Введите значение')
        self.lb3 = QLabel('Выберите категорию')

        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input3 = QComboBox()

        self.input3.addItems(['1', '2', '3'])

        self.btn1 = QPushButton('Добавить слово')
        self.btn2 = QPushButton('Добавление слов')
        self.btn3 = QPushButton('Повторение слов')
        self.btn4 = QPushButton('Вывести все слова')

        self.btn2.clicked.connect(self.changeToAdd)
        self.btn3.clicked.connect(self.changeToRep)

        self.btn4.clicked.connect(self.print_all_words)

        self.word_list = QListWidget()

        self.vlo1 = QVBoxLayout()
        self.vlo2 = QVBoxLayout()
        self.vlo3 = QVBoxLayout()
        self.hlo1 = QHBoxLayout()



        self.vlo_enter = QVBoxLayout()
        self.show_la = QHBoxLayout()
        self.main_layout = QVBoxLayout()

        # Заполняем блоки элементами
        self.vlo1.addWidget(self.lb1)
        self.vlo1.addWidget(self.input1)

        self.vlo2.addWidget(self.lb2)
        self.vlo2.addWidget(self.input2)

        self.vlo3.addWidget(self.lb3)
        self.vlo3.addWidget(self.input3)

    
        self.hlo1.addWidget(self.btn3)
        self.hlo1.addWidget(self.btn4)

        self.vlo_enter.addLayout(self.vlo1)
        self.vlo_enter.addLayout(self.vlo2)
        self.vlo_enter.addLayout(self.vlo3)
        self.vlo_enter.addWidget(self.btn1)

        self.show_la.addWidget(self.word_list)
        self.show_la.addLayout(self.vlo_enter)

        self.main_layout.addLayout(self.show_la)
        self.main_layout.addLayout(self.hlo1)

        self.btn1.clicked.connect(self.printInfo)


        res_View = self.main_layout
        return res_View
    

    def changeToRep(self):
        first_view = self.renderRep()
        # Итоговая компановка и вывод
        widget = QWidget()
        widget.setLayout(first_view)
        self.setCentralWidget(widget)


    def changeToAdd(self):
        first_view = self.renderAdd()
        # Итоговая компановка и вывод
        widget = QWidget()
        widget.setLayout(first_view)
        self.setCentralWidget(widget)
    

    def printInfo(self):
        word_in = self.input1.text()
        defi = self.input2.text()
        cate = self.input3.currentText()

        dict_rec = word_in + ' | ' + defi + ' | ' + cate

        self.word_list.addItem(dict_rec)
        Words.create(word = word_in, desc = defi, category = cate)
    
    def print_all_words(self):
        all_words = list(Words.select().dicts())
        for word in all_words:
            out = f'id {word['id']}, word {word['word']}, description {word['desc']}, category {word['category']}'
            self.word_list.addItem(out)

    def get_word(self):
        all_words = list(Words.select())

        random_word = random.choice(all_words)

        return random_word.word, random_word.desc
    
    def check_answer(self):
        ans = self.input1.text().strip()
        if ans == self.true_ans:
            self.lb5.setText('Правильно! :)')
        else:
            self.lb5.setText(f'''Не правильно :( 
Правильный ответ: {self.true_ans}''')



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()