#to do it
#Сделать список дел [дата, дело, приоритетность, отметка о выполнении(1, 0)]
import os
import sys
from datetime import date
from peewee import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QScrollArea, QMainWindow, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt


filename = 'tasks.db'
db = SqliteDatabase(filename)


#класс стандартной автоматической модели для бд
class BaseModel(Model):
    class Meta:
        database = db


#Класс задач
class Task(BaseModel):
    id = AutoField(primary_key = True)
    username = CharField(max_length = 100)
    task = TextField()
    priority = IntegerField()
    date = DateField(default = date.today)
    category = CharField(max_length = 100)
    active = BooleanField(default = True)
    class Meta:
        table_name = 'users'

#Создание таблицы в бд
if os.path.exists(filename):
    pass
else:
    db.create_tables([Task])



#Выход в hub
def exitter():
    ex = input('Введите hub чтобы выйти ')
    if ex == 'hub':
        return False
    else:
        return True
    

#Создание новой задачи
def create_new_task():
    while exitter():
        task_name = input('Введите задачу ')
        prior = int(input('Введите приоритет '))
        task_date = input('Введите дату выполнения в формате ГГГГ-ММ-ДД ')
        categ = input('Введите категорию ') 
        if check_task(start_user, task_name): #проверка на повтор
            task = Task.create(username = start_user, task = task_name, priority = prior, date = task_date, category = categ)



#Проверка на повторение задачи
def check_task(in_user, in_task):
    users = Task.select().where((Task.username == in_user) & (Task.task == in_task) & (Task.active == True)).exists()
    if users:
        print('Такая задача уже существует')
        return False
    return True



#Получение даты пользователя
def get_user_time():
    return date.today()


#Вывод всех задач заданной категории
def show_category(categ):
    all_category = Task.select().where((Task.username == start_user) & (Task.category == categ) & (Task.active == True))
    for task in all_category: 
        print(f'{task.task} {task.priority} {task.date} {task.category}')



#Вывод всех активных задач по приоритету
def show_all_task_by_priority():
    all_tasks = Task.select().where((Task.username == start_user) & (Task.active == True)).order_by(Task.priority.asc())
    for task in all_tasks: 
        print(f'Задача - {task.task}; Приоритет - {task.priority}; Дата выполнения - {task.date}; Категория - {task.category}; Статус: В работе')


#Уведомление
def notification(curr_date):
    today_tasks = Task.select().where((Task.username == start_user) & (Task.active == True) & (Task.date == curr_date))
    tasks_output = []
    for task in today_tasks: 
        print(f'Задачи на сегодня:\n{task.task} {task.priority} {task.date} {task.category}')
        tasks_output.append(f'{task.task} {task.priority} {task.date} {task.category}')

    ntfc_window = QWidget()
    ntfc_window.setWindowTitle("Невыполненные задачи на сегодня")
    ntfc_window.resize(400, 300)

    ntfc_window.setLayout(QVBoxLayout())
    ntfc_window.layout().addWidget(QLabel("Уведомление"))

    ntfc_window.show()
    return

#Перезапись задачи
def update_task(task_name, new_task_name):
    Task.update(task = new_task_name).where((Task.username == start_user) & (Task.task == task_name)).execute()

#Удаление задачи
def delete_task(task_name):
    Task.delete().where((Task.username == start_user) & (Task.task == task_name)).execute()


#Отметка о выполнении
def update_done(task_name):
    print(task_name)
    Task.update(active = False).where((Task.username == start_user) & (Task.task == task_name)).execute()


#удаление всех задач пользователя, только для админа
def delete_user(user):
    Task.delete().where((Task.username == user)).execute()


def get_start_user():
    user_window = QWidget()
    user_window.setWindowTitle("Вход")
    user_window.resize(300, 150)

    layout = QVBoxLayout()

    layout.addWidget(QLabel("Введите имя пользователя: "))
    user_input = QLineEdit()
    layout.addWidget(user_input)
    def on_login():
        global start_user 
        start_user = user_input.text()
        if start_user:
            user_window.close()
            main()
        else:
            QMessageBox.warning(user_window, "Error")
    enter_button = QPushButton("Войти")
    enter_button.clicked.connect(on_login)
    layout.addWidget(user_window)
    user_window.setLayout(layout)
    user_window.show()
    return user_window



app = QApplication(sys.argv)
#Основная программа
def main():
    main_window = QMainWindow()
    main_window.setWindowTitle("Задачник")
    main_window.resize(600, 500)

    main_buttons = QWidget()
    main_window.setCentralWidget(main_buttons)

    layout = QVBoxLayout()

    text_output = QTextEdit()
    text_output.setReadOnly(True)

    commands = '''
Возможные команды:
Добавить задачу
Просмотр задач по категории
Показать все задачи
Изменить задачу
Отметить задачу выполненной
Удалить задачу
Удалить пользователя
'''

    text_output.setText(commands)

    all_buttons = [("Добавить задачу", lambda: create_new_task(text_output)),
                    ("Просмотр задач по категории",lambda: show_category(text_output)),
                    ("Показать все задачи", lambda: show_all_task_by_priority(text_output)),
                    ("Изменить задачу", lambda: update_task(text_output)),
                    ("Отметить задачу выполненной", lambda: update_done(text_output)),
                    ("Удалить задачу", lambda: delete_task(text_output))]
    if start_user == 'admin':
        all_buttons.append(("Удалить пользователя", lambda: delete_user(text_output)))
    
    for button_text, command in all_buttons:
        button = QPushButton(button_text)
        button.clicked.connect(command)
        layout.addWidget(button)
    main_window.setLayout(layout)
    main_window.show()

    notification(get_user_time()) #Уведомление о невыполненных задачах на текущий день

get_start_user()

sys.exit(app.exec_())
db.close()