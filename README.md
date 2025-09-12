# 🐍 PyQt5 Python аналог(VsCode)

Этот проект — простой текстовый редактор на [PyQt5](https://pypi.org/project/PyQt5/),  
в котором реализована подсветка синтаксиса языка Python.

---

## ✨ Возможности
- Подсветка ключевых слов Python (`def`, class, if, else, и т. д.)
- Подсветка строк (`"..."`, `'...'`)
- Подсветка комментариев (`# ...`)
- Подсветка чисел (`123`, `42`)
- Простое подключение к любому QPlainTextEdit или QTextEdit

---

## 📦 Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/pyqt5-syntax-highlighter.git
   cd pyqt5-syntax-highlighter

2. Установите зависимости:
    pip install PyQt5

3. Запустите редактор:
    python PyQt5_redaktor.py

📂 Структура проекта
📦 pyqt5-syntax-highlighter
    ┣ 📜 pyqt_style.py          # Класс PythonHighlighter (подсветка синтаксиса)
    ┣ 📜 PyQt5_redaktor.py      # Основное приложение-редактор
    ┗ 📜 README.md              # Документация проекта

🔍 Подробное объяснение кода
📌 Файл: pyqt_style.py
    Этот файл содержит класс PythonHighlighter, который наследует QSyntaxHighlighter
    и описывает правила подсветки.
## Импорты
    from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
    import keyword, re
    * QSyntaxHighlighter — базовый класс подсветки.
    * QTextCharFormat — хранит цвет, шрифт, стиль.
    * QColor, QFont — управление цветами и шрифтами.
    * keyword — список ключевых слов Python.
    * re — регулярные выражения для поиска текста.

## Форматы для элементов
    self.keyword_format = QTextCharFormat()
    self.keyword_format.setForeground(QColor("#569CD6"))
    self.keyword_format.setFontWeight(QFont.Bold)
## Ключевые слова → синие и жирные.
    self.string_format = QTextCharFormat()
    self.string_format.setForeground(QColor("#CE9178"))
## Строки ("...", '...') → коричневые.
    self.comment_format = QTextCharFormat()
    self.comment_format.setForeground(QColor("#6A9955"))
    self.comment_format.setFontItalic(True)
## Комментарии (# ...) → зелёные и курсив.
    self.number_format = QTextCharFormat()
    self.number_format.setForeground(QColor("#B5CEA8"))
## Числа (123) → светло-зелёные.

## Правила подсветки
    keywords = keyword.kwlist + ["print"]
    for kw in keywords:
        pattern = r"\b" + kw + r"\b"
        self.rules.append((re.compile(pattern), self.keyword_format))
    * Берём список ключевых слов Python.
    * Добавляем print (встроенная функция).
    * Создаём правило для каждого слова.
        self.rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), self.string_format))
        self.rules.append((re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), self.string_format))
    * Подсветка строк.
        sf.rules.append((re.compile(r"#.*"), self.comment_format))
    * Подсветка комментариев.
        self.rules.append((re.compile(r"\b[0-9]+\b"), self.number_format))
    * Подсветка чисел.
## Основной метод
    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)
* Запускается автоматически для каждой строки.
* Находит совпадения по регуляркам.
* Применяет стиль (self.setFormat).
📌 Файл: PyQt5_redaktor.py
Главное приложение-редактор с полем для текста.
## Импорты
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit
    import pyqt_style
# QApplication — запуск приложения.
# QMainWindow — главное окно.
# QPlainTextEdit — текстовый редактор.
# pyqt_style — наш модуль подсветки.
## Класс редактора
    class Program(QMainWindow):
        def __init__(self):
            super().__init__()
            self.initUI()
## Создаём главное окно.
Интерфейс
    def initUI(self):
        editor = QPlainTextEdit(self)
        self.setCentralWidget(editor)

        # подключаем подсветку
        highlighter = pyqt_style.PythonHighlighter(editor.document())

        self.setWindowTitle("Редактор с подсветкой")
        self.resize(800, 600)
        self.show()
Создаём текстовое поле.
Передаём его document() в PythonHighlighter.
Устанавливаем заголовок и размер окна.
Точка входа

    if name == "__main__":
        app = QApplication(sys.argv)
        w = Program()
        sys.exit(app.exec_())
        
Запускаем приложение.
Открываем окно редактора.
Работаем до закрытия.


📌 Итог
 • pyqt_style.py — модуль подсветки Python-кода.
 • PyQt5_redaktor.py — минимальный редактор с подключением подсветки.
 • Простой пример IDE-подобного редактора на PyQt5.
