from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QComboBox, 
    QPushButton, QListWidget, QDateEdit, QVBoxLayout, QHBoxLayout
)
from datetime import date


class MainWindow(QMainWindow):
    def __init__(self, logic_handler):
        super().__init__()
        self.logic_handler = logic_handler
        self.current_user = None

        first_view = self.login_user_window()

        widget = QWidget()
        widget.setLayout(first_view)
        self.setCentralWidget(widget)

    def login_user_window(self):
        """Окно входа пользователя"""
        self.lb1 = QLabel('Добро пожаловать в Задачник TDL')
        self.lb2 = QLabel('Введите ваше имя')

        self.input_user = QLineEdit()

        self.btn1 = QPushButton('Продолжить')

        vlo1 = QVBoxLayout()
        
        vlo1.addWidget(self.lb1)
        vlo1.addWidget(self.lb2)
        vlo1.addWidget(self.input_user)
        vlo1.addWidget(self.btn1)

        self.btn1.clicked.connect(self.logic_handler.set_user_and_continue)

        return vlo1

    def add_task_window(self):
        """Главное окно добавления задач"""
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

        vlo1 = QVBoxLayout()
        vlo2 = QVBoxLayout()
        vlo3 = QVBoxLayout()
        vlo4 = QHBoxLayout()
        vlo5 = QVBoxLayout()

        vlo_enter = QVBoxLayout()
        main_layout = QHBoxLayout()
        mainly_layout = QVBoxLayout()

        # Заполняем блоки элементами
        vlo1.addWidget(self.lb1)
        vlo1.addWidget(self.input1)

        vlo2.addWidget(self.lb2)
        vlo2.addWidget(self.input2)

        vlo3.addWidget(self.lb3)
        vlo3.addWidget(self.input3)

        vlo4.addWidget(self.btn2)
        vlo4.addWidget(self.btn3)
        vlo4.addWidget(self.btn4)

        vlo5.addWidget(self.lb4)
        vlo5.addWidget(self.input4)

        vlo_enter.addLayout(vlo1)
        vlo_enter.addLayout(vlo2)
        vlo_enter.addLayout(vlo3)
        vlo_enter.addLayout(vlo5)
        vlo_enter.addWidget(self.btn1)

        main_layout.addWidget(self.word_list)
        main_layout.addLayout(vlo_enter)
        mainly_layout.addLayout(main_layout)
        mainly_layout.addLayout(vlo4)

        # Итоговая компановка и вывод
        widget = QWidget()
        widget.setLayout(mainly_layout)
        self.setCentralWidget(widget)

        # Поведение элементов
        self.btn1.clicked.connect(self.logic_handler.add_task)
        self.btn2.clicked.connect(self.logic_handler.all_user_tasks_window)
        self.btn3.clicked.connect(self.logic_handler.update_task_window)
        self.btn4.clicked.connect(self.logic_handler.task_done_window)
        self.input3.addItems(['1','2','3'])
        self.input4.setDate(date.today())

    def all_user_tasks_window(self, tasks):
        """Окно просмотра всех задач пользователя"""
        self.list_tasks = QListWidget()
        self.btn_exit = QPushButton('Вернуться назад')

        for task in tasks:
            status = "активна" if task.active else "выполнена"
            self.list_tasks.addItem(f"{task.task} | {task.category} | Приоритет: {task.priority} | {task.date} | {status}")

        vlo1 = QVBoxLayout()
        vlo1.addWidget(self.list_tasks)
        vlo1.addWidget(self.btn_exit)

        widget = QWidget()
        widget.setLayout(vlo1)
        self.setCentralWidget(widget)

        self.btn_exit.clicked.connect(self.logic_handler.add_task_window)

    def update_task_window(self):
        """Окно редактирования задачи"""
        # Создаем элементы
        self.lb_title = QLabel('Редактирование задачи')
        self.lb_select_task = QLabel('Выберите задачу для редактирования:')
        self.lb_task = QLabel('Название задачи:')
        self.lb_category = QLabel('Категория:')
        self.lb_priority = QLabel('Приоритет:')
        self.lb_date = QLabel('Дата задачи:')
        
        self.combo_tasks = QComboBox()
        self.input_task = QLineEdit()
        self.input_category = QLineEdit()
        self.combo_priority = QComboBox()
        self.input_date = QDateEdit()
        
        self.btn_update = QPushButton('Обновить задачу')
        self.btn_back = QPushButton('Назад')
        
        # Настройка приоритетов
        self.combo_priority.addItems(['1', '2', '3'])
        
        # Настройка даты
        self.input_date.setDate(date.today())
        
        # Компоновка
        main_layout = QVBoxLayout()
        
        main_layout.addWidget(self.lb_title)
        main_layout.addWidget(self.lb_select_task)
        main_layout.addWidget(self.combo_tasks)
        main_layout.addSpacing(20)
        
        # Поля редактирования
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.lb_task)
        form_layout.addWidget(self.input_task)
        form_layout.addWidget(self.lb_category)
        form_layout.addWidget(self.input_category)
        form_layout.addWidget(self.lb_priority)
        form_layout.addWidget(self.combo_priority)
        form_layout.addWidget(self.lb_date)
        form_layout.addWidget(self.input_date)
        
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)
        
        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_update)
        button_layout.addWidget(self.btn_back)
        
        main_layout.addLayout(button_layout)
        
        # Устанавливаем компоновку
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        
        # Подключаем сигналы
        self.btn_update.clicked.connect(self.logic_handler.update_task)
        self.btn_back.clicked.connect(self.logic_handler.add_task_window)
        self.combo_tasks.currentIndexChanged.connect(self.logic_handler.on_task_selected)

    def task_done_window(self):
        """Окно отметки задачи как выполненной"""
        # Создаем элементы
        self.lb_title = QLabel('Отметка задачи выполненной')
        self.lb_select_task = QLabel('Выберите задачу для отметки о выполнении:')
        
        self.combo_tasks = QComboBox()
        self.btn_done = QPushButton('Отметить выполненной')
        self.btn_back = QPushButton('Назад')
        
        # Компоновка
        main_layout = QVBoxLayout()
        
        main_layout.addWidget(self.lb_title)
        main_layout.addWidget(self.lb_select_task)
        main_layout.addWidget(self.combo_tasks)
        main_layout.addSpacing(20)
        
        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_done)
        button_layout.addWidget(self.btn_back)
        
        main_layout.addLayout(button_layout)
        
        # Устанавливаем компоновку
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        
        # Подключаем сигналы
        self.btn_done.clicked.connect(self.logic_handler.task_done_update)
        self.btn_back.clicked.connect(self.logic_handler.add_task_window)

    def printInfo(self, task_data):
        """Вывод информации о добавленной задаче"""
        task, category, priority, task_date = task_data
        dict_rec = f'{task} | {category} | {priority} | {task_date}'
        self.word_list.addItem(dict_rec)