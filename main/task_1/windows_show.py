from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QComboBox, 
    QPushButton, QListWidget, QVBoxLayout, QHBoxLayout
)


class MainWindow(QMainWindow):
    def __init__(self, logic_handler):
        super().__init__()
        self.logic_handler = logic_handler
        self.current_question = None
        self.true_ans = None
        
        # Показываем главное меню при запуске
        self.show_main_menu()

    def setNewView(self, view):
        widget = QWidget()
        widget.setLayout(view)
        self.setCentralWidget(widget)
    
    def show_main_menu(self):
        """Главное меню приложения"""
        layout = QVBoxLayout()
        
        self.lb_welcome = QLabel('Добро пожаловать в словарь!')
        self.btn_add_words = QPushButton('Добавление слов')
        self.btn_repeat_words = QPushButton('Повторение слов')
        self.btn_view_words = QPushButton('Просмотр всех слов')
        self.btn_edit_words = QPushButton('Редактирование слов')
        self.btn_delete_words = QPushButton('Удаление слов')
        
        layout.addWidget(self.lb_welcome)
        layout.addWidget(self.btn_add_words)
        layout.addWidget(self.btn_repeat_words)
        layout.addWidget(self.btn_view_words)
        layout.addWidget(self.btn_edit_words)
        layout.addWidget(self.btn_delete_words)
        
        self.btn_add_words.clicked.connect(self.logic_handler.renderAdd)
        self.btn_repeat_words.clicked.connect(self.logic_handler.renderRep)
        self.btn_view_words.clicked.connect(self.logic_handler.renderViewAll)
        self.btn_edit_words.clicked.connect(self.logic_handler.renderEdit)
        self.btn_delete_words.clicked.connect(self.logic_handler.renderDelete)
        
        self.setNewView(layout)

    def renderRep(self, word_result):
        """Окно повторения слов"""
        layout = QVBoxLayout()
        
        self.lb_question = QLabel('Слово:')
        
        if word_result:
            self.current_question, self.true_ans = word_result
            self.lb_word = QLabel(self.current_question)
        else:
            self.lb_word = QLabel('Нет слов для повторения')
            self.true_ans = ''
        
        self.lb_answer = QLabel('Введите перевод:')
        self.input_answer = QLineEdit()
        self.lb_result = QLabel('Результат:')
        self.lb_result_text = QLabel('')
        
        self.btn_check = QPushButton('Проверить')
        self.btn_next = QPushButton('Следующее слово')
        self.btn_back = QPushButton('Назад в меню')
        
        layout.addWidget(self.lb_question)
        layout.addWidget(self.lb_word)
        layout.addWidget(self.lb_answer)
        layout.addWidget(self.input_answer)
        layout.addWidget(self.btn_check)
        layout.addWidget(self.lb_result)
        layout.addWidget(self.lb_result_text)
        layout.addWidget(self.btn_next)
        layout.addWidget(self.btn_back)
        
        self.btn_check.clicked.connect(self.logic_handler.check_answer)
        self.btn_next.clicked.connect(self.logic_handler.next_word)
        self.btn_back.clicked.connect(self.show_main_menu)
        
        self.setNewView(layout)

    def renderAdd(self):
        """Окно добавления слов"""
        layout = QVBoxLayout()
        
        self.lb_word = QLabel('Введите слово:')
        self.input_word = QLineEdit()
        self.lb_desc = QLabel('Введите перевод:')
        self.input_desc = QLineEdit()
        self.lb_category = QLabel('Выберите категорию:')
        self.input_category = QComboBox()
        self.input_category.addItems(['Основная', 'Работа', 'Путешествия', 'Еда', 'Другое'])
        
        self.btn_add = QPushButton('Добавить слово')
        self.btn_back = QPushButton('Назад в меню')
        
        self.word_list = QListWidget()
        
        # Разделение на две колонки
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        
        left_layout.addWidget(self.lb_word)
        left_layout.addWidget(self.input_word)
        left_layout.addWidget(self.lb_desc)
        left_layout.addWidget(self.input_desc)
        left_layout.addWidget(self.lb_category)
        left_layout.addWidget(self.input_category)
        left_layout.addWidget(self.btn_add)
        left_layout.addWidget(self.btn_back)
        
        right_layout.addWidget(QLabel('Добавленные слова:'))
        right_layout.addWidget(self.word_list)
        
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        layout.addLayout(main_layout)
        
        self.btn_add.clicked.connect(self.logic_handler.add_word)
        self.btn_back.clicked.connect(self.show_main_menu)
        
        self.setNewView(layout)

    def renderViewAll(self):
        """Окно просмотра всех слов"""
        layout = QVBoxLayout()
        
        self.lb_title = QLabel('Все слова в словаре:')
        self.word_list_all = QListWidget()
        self.btn_back = QPushButton('Назад в меню')
        self.btn_refresh = QPushButton('Обновить список')
        
        layout.addWidget(self.lb_title)
        layout.addWidget(self.word_list_all)
        layout.addWidget(self.btn_refresh)
        layout.addWidget(self.btn_back)
        
        self.btn_back.clicked.connect(self.show_main_menu)
        self.btn_refresh.clicked.connect(self.logic_handler.load_all_words)
        
        self.setNewView(layout)

    def renderEdit(self):
        """Окно редактирования слов"""
        layout = QVBoxLayout()
        
        self.lb_select = QLabel('Выберите слово для редактирования:')
        self.combo_words = QComboBox()
        self.lb_new_word = QLabel('Новое слово:')
        self.input_edit_word = QLineEdit()
        self.lb_new_desc = QLabel('Новый перевод:')
        self.input_edit_desc = QLineEdit()
        self.lb_new_category = QLabel('Новая категория:')
        self.input_edit_category = QComboBox()
        self.input_edit_category.addItems(['Основная', 'Работа', 'Путешествия', 'Еда', 'Другое'])
        
        self.btn_load_word = QPushButton('Загрузить данные слова')
        self.btn_update = QPushButton('Обновить слово')
        self.btn_back = QPushButton('Назад в меню')
        
        layout.addWidget(self.lb_select)
        layout.addWidget(self.combo_words)
        layout.addWidget(self.btn_load_word)
        layout.addWidget(self.lb_new_word)
        layout.addWidget(self.input_edit_word)
        layout.addWidget(self.lb_new_desc)
        layout.addWidget(self.input_edit_desc)
        layout.addWidget(self.lb_new_category)
        layout.addWidget(self.input_edit_category)
        layout.addWidget(self.btn_update)
        layout.addWidget(self.btn_back)
        
        self.btn_load_word.clicked.connect(self.logic_handler.load_word_data)
        self.btn_update.clicked.connect(self.logic_handler.update_word)
        self.btn_back.clicked.connect(self.show_main_menu)
        
        self.setNewView(layout)

    def renderDelete(self):
        """Окно удаления слов"""
        layout = QVBoxLayout()
        
        self.lb_select_del = QLabel('Выберите слово для удаления:')
        self.combo_words_del = QComboBox()
        self.lb_word_info = QLabel('Информация о слове:')
        self.lb_word_details = QLabel('')
        
        self.btn_load_info = QPushButton('Показать информацию')
        self.btn_delete = QPushButton('Удалить слово')
        self.btn_back = QPushButton('Назад в меню')
        
        layout.addWidget(self.lb_select_del)
        layout.addWidget(self.combo_words_del)
        layout.addWidget(self.btn_load_info)
        layout.addWidget(self.lb_word_info)
        layout.addWidget(self.lb_word_details)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_back)
        
        self.btn_load_info.clicked.connect(self.logic_handler.show_word_info)
        self.btn_delete.clicked.connect(self.logic_handler.delete_word)
        self.btn_back.clicked.connect(self.show_main_menu)
        
        self.setNewView(layout)