import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QFileDialog
)


class Program(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Eldos")
        self.resize(500, 400)

        main_layout = QVBoxLayout()

        
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save", self)
        self.new_file_btn = QPushButton("New file", self)
        self.run_btn = QPushButton("Run script", self)

        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.new_file_btn)
        button_layout.addWidget(self.run_btn)
        main_layout.addLayout(button_layout)

        
        self.num3_input = QTextEdit(self)
        main_layout.addWidget(self.num3_input)

        
        button_layout2 = QHBoxLayout()
        self.select_all_btn = QPushButton("Select_all", self)
        self.delete_all_btn = QPushButton("Delete_all", self)

        button_layout2.addWidget(self.select_all_btn)
        button_layout2.addWidget(self.delete_all_btn)
        main_layout.addLayout(button_layout2)

        self.setLayout(main_layout)

       
        self.save_btn.clicked.connect(self.save_file)
        self.new_file_btn.clicked.connect(self.new_file)
        self.run_btn.clicked.connect(self.run_script)
        self.select_all_btn.clicked.connect(self.select_all)
        self.delete_all_btn.clicked.connect(self.delete_all)

        self.show()

    def save_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "",
            "Текстовые файлы (*.txt *.py);;Все файлы (*)", options=options
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    text_to_save = self.num3_input.toPlainText()
                    f.write(text_to_save)
                print(f"Файл сохранён: {file_path}")
            except Exception as e:
                print(f"Ошибка при сохранении файла: {e}")

    def new_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Создать новый файл", "",
            "Текстовые файлы (*.txt *.py);;Все файлы (*)", options=options
        )
        if file_path:
            try:
                self.num3_input.clear()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("")
                print(f"Новый файл создан: {file_path}")
            except Exception as e:
                print(f"Ошибка при создании файла: {e}")

    def run_script(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать Python-скрипт", "",
            "Python файлы (*.py);;Все файлы (*)", options=options
        )
        if file_path:
            try:
                result = subprocess.run(
                    [sys.executable, file_path],
                    capture_output=True, text=True
                )
               
                self.num3_input.setPlainText(
                    f"=== НАЧАЛО ===\n{result.stdout}\n\n=== КОНЕЦ ===\n{result.stderr}"
                )
                print("Скрипт выполнен")
            except Exception as e:
                self.num3_input.setPlainText(f"Ошибка при запуске: {e}")

    def select_all(self):
        """Выделить весь текст"""
        self.num3_input.selectAll()

    def delete_all(self):
        """Удалить весь текст"""
        self.num3_input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Program()
    sys.exit(app.exec_())
