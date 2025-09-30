#to do it
#Сделать список дел [дата, дело, приоритетность, отметка о выполнении(1, 0)]
import os
from datetime import date
from peewee import *

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
    for task in today_tasks: 
        print(f'Задачи на сегодня:\n{task.task} {task.priority} {task.date} {task.category}')


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



#Ввод имени пользователя
start_user = input('Введите имя пользователя ')

#Основная программа
while exitter():
    notification(get_user_time()) #Уведомление о невыполненных задачах на текущий день
    print(#Вывод всех команд
'''
Возможные команды:
1 - добавить новую задачу
2 - показать невыполненные задачи по категории
3 - показать все задачи
4 - изменить название задачи
5 - отметить задачу выполненной
6 - удалить задачу
7 - команда администратора
'''
)
    #перебор по командам
    comand = input('Введите номер команды ')
    if comand == '1':   #Создание новой задачи
        create_new_task()
    elif comand == '2':  #Вывод задач по категории
        show_category(input('Введите категорию для вывода '))
    elif comand == '3':   #Вывод всех невыполненны задач с их характеристиками
        show_all_task_by_priority()
    elif comand == '4': #Изменение задачи 
        input_old_task = input('Введите старое название задачи ')
        input_new_task = input('Введите новое название задачи')
        update_task(input_old_task, input_new_task)
    elif comand == '5':   #Отметка о выполнении задачи
        task_done = input('Введите выполненную задачу ')
        update_done(task_done)
    elif comand == '6':   #Удаление здачи по названию
        d_task = input('Введите задачу, которую нужно удалить ')
        delete_task(d_task)
    elif comand == '7' and start_user == 'admin':  #Команда админа - удаление всех задач пользователя
        d_user = input('Введите пользователя, чьи задачи будут удалены безвозвратно ')
        delete_user(d_user)
    else:
        print('Команда введена неверно')
        continue


db.close()