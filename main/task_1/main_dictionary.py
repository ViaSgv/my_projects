from PySide6.QtWidgets import QApplication, QMessageBox
from peewee import *
import os
import sys
import random
from windows_show import MainWindow


class DatabaseManager:
    def __init__(self, filename='words.db'):
        self.filename = filename
        self.db = SqliteDatabase(filename)
        self.setup_database()

    def setup_database(self):
        class BaseModel(Model):
            class Meta:
                database = self.db

        class Words(BaseModel):
            id = PrimaryKeyField(primary_key=True)
            word = CharField(max_length=100)
            desc = TextField()
            category = CharField(max_length=100)
            
            class Meta:
                table_name = 'word_list'

        self.Words = Words

        if not os.path.exists(self.filename):
            self.db.create_tables([Words])


class LogicHandler:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.Words = self.db_manager.Words
        self.window = None
        self.current_question = None
        self.true_ans = None

    def set_window(self, window):
        self.window = window

    def renderAdd(self):
        self.window.renderAdd()

    def renderRep(self):
        word_result = self.get_word()
        self.window.renderRep(word_result)

    def renderViewAll(self):
        self.window.renderViewAll()
        self.load_all_words()

    def renderEdit(self):
        self.window.renderEdit()
        self.load_words_to_combo()

    def renderDelete(self):
        self.window.renderDelete()
        self.load_words_to_combo_delete()

    def add_word(self):
        """Добавление нового слова"""
        word = self.window.input_word.text().strip()
        desc = self.window.input_desc.text().strip()
        category = self.window.input_category.currentText()
        
        if word and desc:
            # Проверяем, нет ли уже такого слова
            existing_word = self.Words.select().where(self.Words.word == word).first()
            
            if existing_word:
                QMessageBox.warning(self.window, 'Ошибка', 'Такое слово уже существует!')
            else:
                self.Words.create(word=word, desc=desc, category=category)
                self.window.word_list.addItem(f'{word} | {desc} | {category}')
                self.window.input_word.clear()
                self.window.input_desc.clear()
                QMessageBox.information(self.window, 'Успех', 'Слово добавлено!')
        else:
            QMessageBox.warning(self.window, 'Ошибка', 'Заполните все поля!')

    def load_all_words(self):
        """Загрузка всех слов"""
        self.window.word_list_all.clear()
        words = self.Words.select()
        
        if words:
            for word in words:
                self.window.word_list_all.addItem(f'{word.word} - {word.desc} ({word.category})')
        else:
            self.window.word_list_all.addItem('Слова не найдены')

    def load_words_to_combo(self):
        """Загрузка слов в комбобокс для редактирования"""
        self.window.combo_words.clear()
        words = self.Words.select()
        
        for word in words:
            self.window.combo_words.addItem(word.word, word.id)

    def load_words_to_combo_delete(self):
        """Загрузка слов в комбобокс для удаления"""
        self.window.combo_words_del.clear()
        words = self.Words.select()
        
        for word in words:
            self.window.combo_words_del.addItem(word.word, word.id)

    def load_word_data(self):
        """Загрузка данных выбранного слова для редактирования"""
        if self.window.combo_words.currentIndex() >= 0:
            word_id = self.window.combo_words.currentData()
            word = self.Words.get_by_id(word_id)
            
            self.window.input_edit_word.setText(word.word)
            self.window.input_edit_desc.setText(word.desc)
            
            # Устанавливаем категорию
            index = self.window.input_edit_category.findText(word.category)
            if index >= 0:
                self.window.input_edit_category.setCurrentIndex(index)

    def show_word_info(self):
        """Показ информации о выбранном слове"""
        if self.window.combo_words_del.currentIndex() >= 0:
            word_id = self.window.combo_words_del.currentData()
            word = self.Words.get_by_id(word_id)
            
            self.window.lb_word_details.setText(f'Слово: {word.word}\nПеревод: {word.desc}\nКатегория: {word.category}')

    def update_word(self):
        """Обновление слова"""
        if self.window.combo_words.currentIndex() >= 0:
            word_id = self.window.combo_words.currentData()
            new_word = self.window.input_edit_word.text().strip()
            new_desc = self.window.input_edit_desc.text().strip()
            new_category = self.window.input_edit_category.currentText()
            
            if new_word and new_desc:
                # Проверяем, нет ли дубликата (кроме текущего слова)
                existing_word = self.Words.select().where(
                    (self.Words.word == new_word) & (self.Words.id != word_id)
                ).first()
                
                if existing_word:
                    QMessageBox.warning(self.window, 'Ошибка', 'Такое слово уже существует!')
                else:
                    self.Words.update(
                        word=new_word,
                        desc=new_desc,
                        category=new_category
                    ).where(self.Words.id == word_id).execute()
                    
                    QMessageBox.information(self.window, 'Успех', 'Слово обновлено!')
                    self.load_words_to_combo()
            else:
                QMessageBox.warning(self.window, 'Ошибка', 'Заполните все поля!')

    def delete_word(self):
        """Удаление слова"""
        if self.window.combo_words_del.currentIndex() >= 0:
            word_id = self.window.combo_words_del.currentData()
            word_text = self.window.combo_words_del.currentText()
            
            reply = QMessageBox.question(
                self.window, 
                'Подтверждение удаления', 
                f'Вы уверены, что хотите удалить слово "{word_text}"?',
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.Words.delete().where(self.Words.id == word_id).execute()
                QMessageBox.information(self.window, 'Успех', 'Слово удалено!')
                self.load_words_to_combo_delete()
                self.window.lb_word_details.setText('')

    def get_word(self):
        """Получение случайного слова для повторения"""
        words = list(self.Words.select())
        
        if words:
            random_word = random.choice(words)
            return random_word.word, random_word.desc
        return None

    def next_word(self):
        """Следующее слово для повторения"""
        self.renderRep()

    def check_answer(self):
        """Проверка ответа"""
        ans = self.window.input_answer.text().strip()
        if ans == self.window.true_ans:
            self.window.lb_result_text.setText('Правильно! :)')
        else:
            self.window.lb_result_text.setText(f'Не правильно :(\nПравильный ответ: {self.window.true_ans}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    logic_handler = LogicHandler()
    window = MainWindow(logic_handler)
    logic_handler.set_window(window)
    
    window.show()
    app.exec()