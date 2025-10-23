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
    QMessageBox,

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
        
        self.btn_add_words.clicked.connect(self.renderAdd)
        self.btn_repeat_words.clicked.connect(self.renderRep)
        self.btn_view_words.clicked.connect(self.renderViewAll)
        self.btn_edit_words.clicked.connect(self.renderEdit)
        self.btn_delete_words.clicked.connect(self.renderDelete)
        
        self.setNewView(layout)

    def renderRep(self):
        """Окно повторения слов"""
        layout = QVBoxLayout()
        
        self.lb_question = QLabel('Слово:')
        
        # Получаем случайное слово
        word_result = self.get_word()
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
        
        self.btn_check.clicked.connect(self.check_answer)
        self.btn_next.clicked.connect(self.next_word)
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
        
        self.btn_add.clicked.connect(self.add_word)
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
        self.btn_refresh.clicked.connect(self.load_all_words)
        
        # Загружаем слова при открытии окна
        self.load_all_words()
        
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
        
        self.btn_load_word.clicked.connect(self.load_word_data)
        self.btn_update.clicked.connect(self.update_word)
        self.btn_back.clicked.connect(self.show_main_menu)
        
        # Загружаем список слов в комбобокс
        self.load_words_to_combo()
        
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
        
        self.btn_load_info.clicked.connect(self.show_word_info)
        self.btn_delete.clicked.connect(self.delete_word)
        self.btn_back.clicked.connect(self.show_main_menu)
        
        # Загружаем список слов в комбобокс
        self.load_words_to_combo_delete()
        
        self.setNewView(layout)

    def add_word(self):
        """Добавление нового слова"""
        word = self.input_word.text().strip()
        desc = self.input_desc.text().strip()
        category = self.input_category.currentText()
        
        if word and desc:
            # Проверяем, нет ли уже такого слова
            existing_word = Words.select().where(Words.word == word).first()
            
            if existing_word:
                QMessageBox.warning(self, 'Ошибка', 'Такое слово уже существует!')
            else:
                Words.create(word=word, desc=desc, category=category)
                self.word_list.addItem(f'{word} | {desc} | {category}')
                self.input_word.clear()
                self.input_desc.clear()
                QMessageBox.information(self, 'Успех', 'Слово добавлено!')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля!')

    def load_all_words(self):
        """Загрузка всех слов"""
        self.word_list_all.clear()
        words = Words.select()
        
        if words:
            for word in words:
                self.word_list_all.addItem(f'{word.word} - {word.desc} ({word.category})')
        else:
            self.word_list_all.addItem('Слова не найдены')

    def load_words_to_combo(self):
        """Загрузка слов в комбобокс для редактирования"""
        self.combo_words.clear()
        words = Words.select()
        
        for word in words:
            self.combo_words.addItem(word.word, word.id)

    def load_words_to_combo_delete(self):
        """Загрузка слов в комбобокс для удаления"""
        self.combo_words_del.clear()
        words = Words.select()
        
        for word in words:
            self.combo_words_del.addItem(word.word, word.id)

    def load_word_data(self):
        """Загрузка данных выбранного слова для редактирования"""
        if self.combo_words.currentIndex() >= 0:
            word_id = self.combo_words.currentData()
            word = Words.get_by_id(word_id)
            
            self.input_edit_word.setText(word.word)
            self.input_edit_desc.setText(word.desc)
            
            # Устанавливаем категорию
            index = self.input_edit_category.findText(word.category)
            if index >= 0:
                self.input_edit_category.setCurrentIndex(index)

    def show_word_info(self):
        """Показ информации о выбранном слове"""
        if self.combo_words_del.currentIndex() >= 0:
            word_id = self.combo_words_del.currentData()
            word = Words.get_by_id(word_id)
            
            self.lb_word_details.setText(f'Слово: {word.word}\nПеревод: {word.desc}\nКатегория: {word.category}')

    def update_word(self):
        """Обновление слова"""
        if self.combo_words.currentIndex() >= 0:
            word_id = self.combo_words.currentData()
            new_word = self.input_edit_word.text().strip()
            new_desc = self.input_edit_desc.text().strip()
            new_category = self.input_edit_category.currentText()
            
            if new_word and new_desc:
                # Проверяем, нет ли дубликата (кроме текущего слова)
                existing_word = Words.select().where(
                    (Words.word == new_word) & (Words.id != word_id)
                ).first()
                
                if existing_word:
                    QMessageBox.warning(self, 'Ошибка', 'Такое слово уже существует!')
                else:
                    Words.update(
                        word=new_word,
                        desc=new_desc,
                        category=new_category
                    ).where(Words.id == word_id).execute()
                    
                    QMessageBox.information(self, 'Успех', 'Слово обновлено!')
                    self.load_words_to_combo()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Заполните все поля!')

    def delete_word(self):
        """Удаление слова"""
        if self.combo_words_del.currentIndex() >= 0:
            word_id = self.combo_words_del.currentData()
            word_text = self.combo_words_del.currentText()
            
            reply = QMessageBox.question(
                self, 
                'Подтверждение удаления', 
                f'Вы уверены, что хотите удалить слово "{word_text}"?',
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                Words.delete().where(Words.id == word_id).execute()
                QMessageBox.information(self, 'Успех', 'Слово удалено!')
                self.load_words_to_combo_delete()
                self.lb_word_details.setText('')

    def get_word(self):
        """Получение случайного слова для повторения"""
        words = list(Words.select())
        
        if words:
            random_word = random.choice(words)
            return random_word.word, random_word.desc
        return None

    def next_word(self):
        """Следующее слово для повторения"""
        self.renderRep()

    def check_answer(self):
        """Проверка ответа"""
        ans = self.input_answer.text().strip()
        if ans == self.true_ans:
            self.lb_result_text.setText('Правильно! :)')
        else:
            self.lb_result_text.setText(f'Не правильно :(\nПравильный ответ: {self.true_ans}')


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()