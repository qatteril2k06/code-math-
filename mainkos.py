import sys
import os
import shutil
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QLabel, QDialog, QDialogButtonBox,
    QVBoxLayout, QGridLayout, QSizePolicy, QScrollArea, QMainWindow,
    QFrame, QHBoxLayout, QFileDialog
)
from math import ceil
from word_counter import word_counter

# Проверка директории themes/ на наличие тем
themes = next(os.walk('themes/'), (None, None, []))[2]

# Функция для очистки директории 'files_to_parse/'
def files_to_parse_clean():
    for root, dirs, files in os.walk('files_to_parse/'):
        for file in files:
            os.remove(os.path.join(root, file))

# Очистка директории 'files_to_parse/' при запуске скрипта
files_to_parse_clean()

# Списки для хранения файлов для анализа и тем
files_to_parse = []
parsed_themes = []

# Диалоговое окно для подтверждения удаления элемента
class AskDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Удаление?')

        q_btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.ok_btn = QDialogButtonBox(q_btn)
        self.ok_btn.accepted.connect(self.accept)
        self.ok_btn.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel('Хотите удалить этот элемент?')
        self.layout.addWidget(message)
        self.layout.addWidget(self.ok_btn)
        self.setLayout(self.layout)

# Диалоговое окно для вывода предупреждения об ошибке при выборе неверного файла
class ErrorFileDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Предупреждение')

        q_btn = QDialogButtonBox.Ok

        self.ok_btn = QDialogButtonBox(q_btn)
        self.ok_btn.accepted.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel('Некорректный файл!')
        self.layout.addWidget(message)
        self.layout.addWidget(self.ok_btn)
        self.setLayout(self.layout)

# Виджет для главного графического интерфейса
class GraphicsMW(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(800, 400, 500, 400)
        self.setWindowTitle('Классификатор текста')

        self.text_input = QLineEdit(self)

        self.text_input.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.text_input.setAlignment(Qt.AlignCenter)
        self.text_input.setFont(QFont('Libel Suit', 14))
        self.text_input.setPlaceholderText('Введите текст здесь')

        self.files_btn = QPushButton('Обзор файлов', self)
        self.files_btn.setFont(QFont('Libel Suit', 15))

        self.themes_btn = QPushButton('Добавить темы', self)
        self.themes_btn.setFont(QFont('Libel Suit', 15))

        self.classify_btn = QPushButton('Классифицировать', self)  # Кнопка ввода
        self.classify_btn.setFont(QFont('Libel Suit Regular', 15))

        self.layout = QGridLayout()  # Создание макета
        self.layout.addWidget(self.text_input, 0, 0, 2, 5)
        self.layout.setHorizontalSpacing(20)
        self.layout.setVerticalSpacing(20)
        self.layout.addWidget(self.files_btn, 2, 0, 1, 2)
        self.layout.addWidget(self.themes_btn, 2, 2, 1, 2)
        self.layout.addWidget(self.classify_btn, 2, 4, 1, 1)
        self.setLayout(self.layout)

# Главное окно, наследующееся от GraphicsMW
class MainWindow(GraphicsMW):
    def __init__(self):
        super().__init__()

        self.files_window = None
        self.themes_window = None
        
        self.classification_window = None

        self.files_btn.clicked.connect(self.files)
        self.themes_btn.clicked.connect(self.themes)
        self.classify_btn.clicked.connect(self.classify)

    # Метод для обработки нажатия кнопки 'Обзор файлов'
    def files(self):
        self.files_window = FilesWindow()

    # Метод для обработки нажатия кнопки 'Добавить темы'
    def themes(self):
        self.themes_window = ThemesWindow()

    # Метод для обработки нажатия кнопки 'Классифицировать'
    def classify(self):
        text = self.text_input.text()
        counted_words = []
        if text:
            with open('input_file/input_file.txt', 'w+', encoding='utf8') as file:
                for line in text.split('\n'):
                    file.write(line)
            counted_words.append(word_counter('input_file/', ['input_file.txt']))
        counted_words.append(word_counter('files_to_parse/', files_to_parse))

        self.classification_window = ClassificationWindow()

# Класс для окна 'Файлы для классификации'
class FilesWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(1000, 300, 620, 300)
        self.setWindowTitle('Файлы для классификации')

        self.scroll = QScrollArea()

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.widget = QWidget()

        self.create_buttons()

        self.initUI()

    # Метод для создания кнопок файлов
    def create_buttons(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        btns_in_row = 6
        positions = [(i, j)
                     for i in range(ceil(len(files_to_parse) / btns_in_row))
                     for j in range(btns_in_row)]
        last_pos = (0, 0)
        for pos, name in zip(positions, files_to_parse):
            button = QPushButton(name)
            frame = QFrame()
            button.clicked.connect(
                lambda ch, btn=button, w=frame: self.interaction(w, btn)
            )

            hbox = QHBoxLayout(frame)
            hbox.addWidget(button)
            self.layout.addWidget(frame, *pos)
            if name == files_to_parse[-1]:
                last_pos = (pos[0] + int(not ((pos[1] + 1) % btns_in_row)),
                            (pos[1] + 1) % btns_in_row)

        adding_btn = QPushButton('+')
        frame = QFrame()
        adding_btn.clicked.connect(self.add)

        hbox = QHBoxLayout(frame)
        hbox.addWidget(adding_btn)

        self.layout.addWidget(frame, *last_pos)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

    # Метод для добавления файла
    def add(self):
        path, ok_pressed = QFileDialog.getOpenFileName(self, 'Выберите тему', '')
        name = path.split('/')[-1]
        if ok_pressed:
            try:
                with open(path, encoding='utf8') as file:
                    text = file
                if name in files_to_parse or \
                        name.split('.')[-1] != 'txt' and len(name.split('.')) > 1:
                    dlg = ErrorFileDialog()
                    dlg.exec()
                else:
                    shutil.copy2(path, f'files_to_parse/{name}')
                    files_to_parse.append(name)
                    self.create_buttons()
            except Exception:
                dlg = ErrorFileDialog()
                dlg.exec()

    # Метод для взаимодействия с кнопкой (например, удаление файла)
    def interaction(self, frame, btn):
        dlg = AskDialog()
        if dlg.exec():
            text = btn.text()
            os.remove(os.path.join('files_to_parse', text))
            files_to_parse.remove(text)
            frame.deleteLater()
            self.create_buttons()

    def initUI(self):
        self.show()

# Класс для окна 'Список всех тем'
class ThemesWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(1000, 300, 200, 300)
        self.setWindowTitle('Список всех тем')

        self.scroll = QScrollArea()

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.widget = QWidget()

        self.create_buttons()

        self.initUI()

    # Метод для создания кнопок тем
    def create_buttons(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        btns_in_row = 1
        positions = [(i, j)
                     for i in range(len(themes))
                     for j in range(btns_in_row)]
        last_pos = (0, 0)
        for pos, name in zip(positions, themes):
            button = QPushButton(name)
            frame = QFrame()
            button.clicked.connect(
                lambda ch, btn=button, w=frame: self.interaction(w, btn)
            )

            hbox = QHBoxLayout(frame)
            hbox.addWidget(button)
            self.layout.addWidget(frame, *pos)
            if name == themes[-1]:
                last_pos = (pos[0] + int(not ((pos[1] + 1) % btns_in_row)),
                            (pos[1] + 1) % btns_in_row)

        adding_btn = QPushButton('+')
        frame = QFrame()
        adding_btn.clicked.connect(self.add)

        hbox = QHBoxLayout(frame)
        hbox.addWidget(adding_btn)

        self.layout.addWidget(frame, *last_pos)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

    # Метод для добавления темы
    def add(self):
        name, ok_pressed = QFileDialog.getOpenFileName(self, 'Выберите тему', '')
        if ok_pressed:
            try:
                with open(name, encoding='utf8') as file:
                    theme = file
                if name in themes:
                    dlg = ErrorFileDialog()
                    dlg.exec()
                else:
                    path = name
                    name = name.split('/')[-1]
                    shutil.copy2(path, f'themes/{name}')
                    themes.append(name)
                    self.create_buttons()
            except Exception:
                dlg = ErrorFileDialog()
                dlg.exec()

    # Метод для взаимодействия с кнопкой (например, удаление темы)
    def interaction(self, frame, btn):
        dlg = AskDialog()
        if dlg.exec():
            theme = btn.text()
            os.remove(os.path.join('themes', theme))
            themes.remove(theme)
            frame.deleteLater()
            self.create_buttons()

    def initUI(self):
        self.show()

# Класс для окна 'Классификация'
class ClassificationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(1000, 300, 200, 300)
        self.setWindowTitle('Классификация')

        self.scroll = QScrollArea()

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.widget = QWidget()

        self.create_themes()

        self.initUI()

    # Метод для создания тем в окне классификации
    def create_themes(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        files_in_raw = 1
        files_positions = [(i, 0)
                           for i in range(len(files_to_parse))
                           for _ in range(files_in_raw)]
        themes_positions = [(i, 1)
                            for i in range(len(files_to_parse))
                            for _ in range(files_in_raw)]

        for file_pos, theme_pos, filename, themename \
                in zip(files_positions, themes_positions, files_to_parse, parsed_themes):
            filename = QLabel(filename)
            filename.setFont(QFont('Libel Suit', 15))
            frame = QFrame()

            hbox = QHBoxLayout(frame)
            hbox.addWidget(filename)
            self.layout.addWidget(frame, *file_pos)

            themename = QLabel(themename)
            themename.setFont(QFont('Libel Suit', 15))
            frame = QFrame()

            hbox = QHBoxLayout(frame)
            hbox.addWidget(themename)
            self.layout.addWidget(frame, *theme_pos)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        files_to_parse.clear()

    def initUI(self):
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()

    sys.exit(app.exec_())
