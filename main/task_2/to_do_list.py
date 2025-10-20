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
    QDateEdit,

    # Организующие элементы
    QVBoxLayout,
    QHBoxLayout
    
)

from datetime import date
from peewee import *
import os
import sys
import random


filename = 'tasks.db'
db = SqliteDatabase(filename)


class BaseModel(Model):
    class Meta:
        database = db


class Words(BaseModel):
    id = PrimaryKeyField(primary_key = True)
    user = CharField(max_length=100)
    task = TextField()
    category = CharField(max_length=100)
    priority = IntegerField()
    date = DateField(default=date.today)
    active = BooleanField(default = True)
    class Meta:
        table_name = 'task_list'


if os.path.exists(filename):
    pass
else:
    db.create_tables([Words])


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()


        # Создаем элементы
        self.lb1 = QLabel('Введите задачу')
        self.lb2 = QLabel('Введите категорию')
        self.lb3 = QLabel('Выберите приоритет')
        self.lb4 = QLabel('Выберите дату задачи')

        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input3 = QComboBox()
        self.input4 = QDateEdit()

        self.btn1 = QPushButton('Добавить задачу')
        self.btn2 = QPushButton('Редактировать задачу')
        self.btn3 = QPushButton('Отметить задачу выполненной')

        self.word_list = QListWidget()

        self.vlo1 = QVBoxLayout()
        self.vlo2 = QVBoxLayout()
        self.vlo3 = QVBoxLayout()
        self.vlo4 = QHBoxLayout()
        self.vlo5 = QVBoxLayout()


        self.vlo_enter = QVBoxLayout()
        self.main_layout = QHBoxLayout()
        self.mainly_layout = QVBoxLayout()
        self.vlo2_enter = QHBoxLayout()

        # Заполняем блоки элементами
        self.vlo1.addWidget(self.lb1)
        self.vlo1.addWidget(self.input1)

        self.vlo2.addWidget(self.lb2)
        self.vlo2.addWidget(self.input2)

        self.vlo3.addWidget(self.lb3)
        self.vlo3.addWidget(self.input3)

        self.vlo4.addWidget(self.btn2)
        self.vlo4.addWidget(self.btn3)

        self.vlo5.addWidget(self.lb4)
        self.vlo5.addWidget(self.input4)

        self.vlo_enter.addLayout(self.vlo1)
        self.vlo_enter.addLayout(self.vlo2)
        self.vlo_enter.addLayout(self.vlo3)
        self.vlo_enter.addLayout(self.vlo5)
        self.vlo_enter.addWidget(self.btn1)

        self.main_layout.addWidget(self.word_list)
        self.main_layout.addLayout(self.vlo_enter)
        self.mainly_layout.addLayout(self.main_layout)
        self.mainly_layout.addLayout(self.vlo4)

        # Итоговая компановка и вывод
        widget = QWidget()
        widget.setLayout(self.mainly_layout)
        self.setCentralWidget(widget)


        # Поведение элементов
        self.btn1.clicked.connect(self.printInfo)
        self.btn1.mouseDoubleClickEvent = lambda p: self.word_list.addItem('Двойной клик!')
        self.input3.addItems(['1','2','3'])

    def printInfo(self):
        word = self.input1.text()
        defi = self.input2.text()
        cate = self.input3.currentText()

        dict_rec = f'{word} | {defi} | {cate}'

        self.word_list.addItem(dict_rec)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()