from PySide6.QtWidgets import QApplication, QMessageBox
from peewee import *
import os
import sys
from datetime import date
from windows_show import MainWindow


class DatabaseManager:
    def __init__(self, filename='tasks.db'):
        self.filename = filename
        self.db = SqliteDatabase(filename)
        self.setup_database()

    def setup_database(self):
        class BaseModel(Model):
            class Meta:
                database = self.db

        class Words(BaseModel):
            id = PrimaryKeyField(primary_key=True)
            user = CharField(max_length=100)
            task = TextField()
            category = CharField(max_length=100)
            priority = IntegerField()
            date = DateField(default=date.today)
            active = BooleanField(default=True)
            
            class Meta:
                table_name = 'task_list'

        self.Words = Words

        if not os.path.exists(self.filename):
            self.db.connect()
            self.db.create_tables([Words])


class LogicHandler:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.Words = self.db_manager.Words
        self.window = None
        self.current_user = None

    def set_window(self, window):
        self.window = window

    def set_user_and_continue(self):
        """Установка пользователя и переход к главному окну"""
        self.current_user = self.window.input_user.text()
        if self.current_user:
            self.window.add_task_window()
        else:
            QMessageBox.warning(self.window, 'Ошибка', 'Введите имя пользователя!')

    def add_task_window(self):
        """Переход к окну добавления задач"""
        if not self.current_user:
            QMessageBox.warning(self.window, 'Ошибка', 'Сначала войдите в систему!')
            return
            
        self.window.add_task_window()

    def add_task(self):
        """Добавление новой задачи"""
        if not self.current_user:
            QMessageBox.warning(self.window, 'Ошибка', 'Сначала войдите в систему!')
            return

        if self.check_task():
            task_name = self.window.input1.text()
            category = self.window.input2.text()
            priority = int(self.window.input3.currentText())
            task_date = self.window.input4.date().toPython()
            
            self.Words.create(
                user=self.current_user, 
                task=task_name, 
                category=category, 
                priority=priority, 
                date=task_date
            )
            
            # Вывод информации о задаче
            task_data = (task_name, category, priority, task_date.strftime('%Y-%m-%d'))
            self.window.printInfo(task_data)
            
            # Очистка полей ввода
            self.window.input1.clear()
            self.window.input2.clear()
            
            QMessageBox.information(self.window, 'Успех', 'Задача добавлена!')

    def check_task(self):
        """Проверка существования задачи"""
        task = self.window.input1.text()
        if not task:
            QMessageBox.warning(self.window, 'Ошибка', 'Введите задачу!')
            return False
            
        exists = self.Words.select().where(
            (self.Words.user == self.current_user) & 
            (self.Words.task == task) & 
            (self.Words.active == True)
        ).exists()
        
        if exists:
            QMessageBox.warning(self.window, 'Ошибка', 'Такая задача уже существует!')
            return False
        return True

    def all_user_tasks_window(self):
        """Отображение всех задач пользователя"""
        if not self.current_user:
            QMessageBox.warning(self.window, 'Ошибка', 'Сначала войдите в систему!')
            return

        tasks = self.Words.select().where(self.Words.user == self.current_user)
        self.window.all_user_tasks_window(tasks)

    def update_task_window(self):
        """Отображение окна редактирования задачи"""
        if not self.current_user:
            QMessageBox.warning(self.window, 'Ошибка', 'Сначала войдите в систему!')
            return

        self.window.update_task_window()
        self.load_tasks_to_combo()

    def task_done_window(self):
        """Отображение окна отметки задачи как выполненной"""
        if not self.current_user:
            QMessageBox.warning(self.window, 'Ошибка', 'Сначала войдите в систему!')
            return

        self.window.task_done_window()
        self.load_active_tasks_to_combo()

    def load_tasks_to_combo(self):
        """Загружает задачи пользователя в комбобокс"""
        self.window.combo_tasks.clear()
        tasks = self.Words.select().where(
            (self.Words.user == self.current_user) & 
            (self.Words.active == True)
        )
        
        for task in tasks:
            self.window.combo_tasks.addItem(f"{task.task} | {task.category}", task.id)

    def load_active_tasks_to_combo(self):
        """Загружает только активные задачи пользователя в комбобокс"""
        self.window.combo_tasks.clear()
        tasks = self.Words.select().where(
            (self.Words.user == self.current_user) & 
            (self.Words.active == True)
        )
        
        for task in tasks:
            self.window.combo_tasks.addItem(f"{task.task} | {task.category} | Приоритет: {task.priority}", task.id)

    def on_task_selected(self):
        """Заполняет поля данными выбранной задачи"""
        if self.window.combo_tasks.currentIndex() >= 0:
            task_id = self.window.combo_tasks.currentData()
            if task_id:
                task = self.Words.get_by_id(task_id)
                
                self.window.input_task.setText(task.task)
                self.window.input_category.setText(task.category)
                self.window.combo_priority.setCurrentText(str(task.priority))
                self.window.input_date.setDate(task.date)

    def update_task(self):
        """Обновляет задачу в базе данных"""
        if self.window.combo_tasks.currentIndex() >= 0:
            task_id = self.window.combo_tasks.currentData()
            if not task_id:
                QMessageBox.warning(self.window, 'Ошибка', 'Выберите задачу для редактирования!')
                return
                
            new_task = self.window.input_task.text().strip()
            new_category = self.window.input_category.text().strip()
            new_priority = int(self.window.combo_priority.currentText())
            new_date = self.window.input_date.date().toPython()
            
            if new_task and new_category:
                # Проверяем, нет ли дубликата (кроме текущей задачи)
                existing_task = self.Words.select().where(
                    (self.Words.task == new_task) & 
                    (self.Words.user == self.current_user) & 
                    (self.Words.id != task_id) &
                    (self.Words.active == True)
                ).first()
                
                if existing_task:
                    QMessageBox.warning(self.window, 'Ошибка', 'Такая задача уже существует!')
                else:
                    self.Words.update(
                        task=new_task,
                        category=new_category,
                        priority=new_priority,
                        date=new_date
                    ).where(self.Words.id == task_id).execute()
                    
                    QMessageBox.information(self.window, 'Успех', 'Задача обновлена!')
                    self.load_tasks_to_combo()
            else:
                QMessageBox.warning(self.window, 'Ошибка', 'Заполните все поля!')
        else:
            QMessageBox.warning(self.window, 'Ошибка', 'Выберите задачу для редактирования!')

    def task_done_update(self):
        """Отмечает задачу как выполненную"""
        if self.window.combo_tasks.currentIndex() >= 0:
            task_id = self.window.combo_tasks.currentData()
            if not task_id:
                QMessageBox.warning(self.window, 'Ошибка', 'Выберите задачу для отметки!')
                return
            
            # Подтверждение действия
            reply = QMessageBox.question(
                self.window, 
                'Подтверждение', 
                'Вы уверены, что хотите отметить задачу как выполненную?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.Words.update(active=False).where(self.Words.id == task_id).execute()
                
                QMessageBox.information(self.window, 'Успех', 'Задача отмечена как выполненная!')
                
                # Обновляем список задач и возвращаемся к основному окну
                self.load_active_tasks_to_combo()
                self.add_task_window()
        else:
            QMessageBox.warning(self.window, 'Ошибка', 'Выберите задачу для отметки!')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    logic_handler = LogicHandler()
    window = MainWindow(logic_handler)
    logic_handler.set_window(window)
    
    window.show()
    app.exec()