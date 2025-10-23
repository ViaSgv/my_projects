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
        self.current_user = None

        first_view = self.login_user_window()

        widget = QWidget()
        widget.setLayout(first_view)
        self.setCentralWidget(widget)

    def add_task_window(self):
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
        self.btn2 = QPushButton('Вывести все мои задачи')
        self.btn3 = QPushButton('Редактировать задачу')
        self.btn4 = QPushButton('Отметить задачу выполненной')

        self.word_list = QListWidget()

        self.vlo1 = QVBoxLayout()
        self.vlo2 = QVBoxLayout()
        self.vlo3 = QVBoxLayout()
        self.vlo4 = QHBoxLayout()
        self.vlo5 = QVBoxLayout()

        self.vlo_enter = QVBoxLayout()
        self.main_layout = QHBoxLayout()
        self.mainly_layout = QVBoxLayout()

        # Заполняем блоки элементами
        self.vlo1.addWidget(self.lb1)
        self.vlo1.addWidget(self.input1)

        self.vlo2.addWidget(self.lb2)
        self.vlo2.addWidget(self.input2)

        self.vlo3.addWidget(self.lb3)
        self.vlo3.addWidget(self.input3)

        self.vlo4.addWidget(self.btn2)
        self.vlo4.addWidget(self.btn3)
        self.vlo4.addWidget(self.btn4)

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
        self.btn1.clicked.connect(self.add_task)
        self.btn2.clicked.connect(self.all_user_tasks_window)
        self.btn3.clicked.connect(self.update_task_window)
        self.btn4.clicked.connect(self.task_done_window)
        self.input3.addItems(['1','2','3'])

    def login_user_window(self):
        self.lb1 = QLabel('Добро пожаловать в Задачник TDL')
        self.lb2 = QLabel('Введите ваше имя')

        self.input_user = QLineEdit()

        self.btn1 = QPushButton('Продолжить')

        self.vlo1 = QVBoxLayout()
        
        self.vlo1.addWidget(self.lb1)
        self.vlo1.addWidget(self.lb2)
        self.vlo1.addWidget(self.input_user)
        self.vlo1.addWidget(self.btn1)

        self.btn1.clicked.connect(self.set_user_and_continue)

        return self.vlo1
    
    def set_user_and_continue(self):
        self.current_user = self.input_user.text()
        self.add_task_window()

    def printInfo(self):
        task = self.input1.text()
        category = self.input2.text()
        priority = self.input3.currentText()
        date = self.input4.text()

        dict_rec = f'{task} | {category} | {priority} | {date}'

        self.word_list.addItem(dict_rec)

    def check_task(self):
        task = self.input1.text()
        users = Words.select().where(
            (Words.user == self.current_user) & 
            (Words.task == task) & 
            (Words.active == True)
        ).exists()
        if users:
            print('Такая задача уже существует')
            return False
        return True
    
    def add_task(self):
        if self.check_task():
            task_name = self.input1.text()
            category = self.input2.text()
            priority = int(self.input3.currentText())
            task_date = self.input4.date().toPython()
            
            Words.create(
                user=self.current_user, 
                task=task_name, 
                category=category, 
                priority=priority, 
                date=task_date
            )
            self.printInfo()
            print("Задача добавлена!")
    
    def all_user_tasks_window(self):
        tasks = Words.select().where(Words.user == self.current_user)
        
        self.list_tasks = QListWidget()
        self.btn_exit = QPushButton('Вернуться назад')

        for task in tasks:
            status = "активна" if task.active else "выполнена"
            self.list_tasks.addItem(f"{task.task} | {task.category} | Приоритет: {task.priority} | {task.date} | {status}")

        self.vlo1 = QVBoxLayout()
        self.vlo1.addWidget(self.list_tasks)
        self.vlo1.addWidget(self.btn_exit)

        widget = QWidget()
        widget.setLayout(self.vlo1)
        self.setCentralWidget(widget)

        self.btn_exit.clicked.connect(self.add_task_window)

    def update_task_window(self):
        self.lb1 = QLabel('Введите название задачи для редактирования')
        self.lb2 = QLabel('Введите новое название задачи')

        self.input_old_task = QLineEdit()
        self.input_new_task = QLineEdit()

        self.btn_update = QPushButton('Подтвердить изменение')
        self.btn_back = QPushButton('Назад')

        self.vlo1 = QVBoxLayout()
        self.vlo2 = QHBoxLayout()

        self.vlo1.addWidget(self.lb1)
        self.vlo1.addWidget(self.input_old_task)
        self.vlo1.addWidget(self.lb2)
        self.vlo1.addWidget(self.input_new_task)
        self.vlo2.addWidget(self.btn_update)
        self.vlo2.addWidget(self.btn_back)
        self.vlo1.addLayout(self.vlo2)

        widget = QWidget()
        widget.setLayout(self.vlo1)
        self.setCentralWidget(widget)

        self.btn_update.clicked.connect(self.update_task)
        self.btn_back.clicked.connect(self.add_task_window)
    
    def update_task(self):
        old_task = self.input_old_task.text()
        new_task = self.input_new_task.text()
        
        Words.update(task=new_task).where(
            (Words.user == self.current_user) & 
            (Words.task == old_task)
        ).execute()
        
        print("Задача обновлена!")
        self.add_task_window()

    def task_done_window(self):
        self.lb1 = QLabel('Введите название задачи для отметки о выполнении')

        self.input_task_done = QLineEdit()

        self.btn_done = QPushButton('Подтвердить выполнение')
        self.btn_back = QPushButton('Назад')

        self.vlo1 = QVBoxLayout()
        self.vlo2 = QHBoxLayout()

        self.vlo1.addWidget(self.lb1)
        self.vlo1.addWidget(self.input_task_done)
        self.vlo2.addWidget(self.btn_done)
        self.vlo2.addWidget(self.btn_back)
        self.vlo1.addLayout(self.vlo2)

        widget = QWidget()
        widget.setLayout(self.vlo1)
        self.setCentralWidget(widget)

        self.btn_done.clicked.connect(self.task_done_update)
        self.btn_back.clicked.connect(self.add_task_window)
    
    def task_done_update(self):
        task_name = self.input_task_done.text()
        
        Words.update(active=False).where(
            (Words.user == self.current_user) & 
            (Words.task == task_name)
        ).execute()
        
        print("Задача отмечена как выполненная!")
        self.add_task_window()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()