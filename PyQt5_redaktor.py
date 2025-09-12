import sys, os, tempfile
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QLabel
)
from PyQt5.QtCore import QProcess, Qt, QSettings
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from pyqt5_style import PythonHighlighter




class CodeEditor(QTextEdit):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            cursor = self.textCursor()
            cursor.movePosition(cursor.StartOfBlock, cursor.KeepAnchor)
            line_text = cursor.selectedText()

            
            indentation = ""
            for ch in line_text:
                if ch == " ":
                    indentation += " "
                elif ch == "\t":
                    indentation += "\t"
                else:
                    break

            super().keyPressEvent(event)

            
            if line_text.strip().endswith(":"):
                self.insertPlainText(indentation + "    ")
            else:
                self.insertPlainText(indentation)
        else:
            super().keyPressEvent(event)


class Program(QWidget):
    def __init__(self):
        super().__init__()
        self.process = None
        self.settings = QSettings("EldosSoft", "EldosIDE")  
        self.dark_mode = self.settings.value("dark_mode", True, type=bool)  
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Eldos IDE Lite")
        self.resize(700, 600)
        

        self.setWindowIcon(QIcon("vscode.png"))

        main_layout = QVBoxLayout()

        
        header_layout = QHBoxLayout()
        title = QLabel("Eldos IDE Lite")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        header_layout.addWidget(title)
        header_layout.addStretch()
        self.theme_btn = QPushButton("", self)
        header_layout.addWidget(self.theme_btn)
        main_layout.addLayout(header_layout)

        
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton(" Save", self)
        self.new_file_btn = QPushButton("New file", self)
        self.run_btn = QPushButton("▶ Run script", self)

        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.new_file_btn)
        button_layout.addWidget(self.run_btn)
        main_layout.addLayout(button_layout)

        
        self.editor = CodeEditor(self)
        self.editor.setPlaceholderText("Введите код здесь...")
        self.editor.setFont(QFont("Consolas", 12))
        main_layout.addWidget(self.editor, 3)

        self.highlighter = PythonHighlighter(self.editor.document())

        
        
        
        button_layout2 = QHBoxLayout()
        self.select_all_btn = QPushButton(" Select_all", self)
        self.delete_all_btn = QPushButton("Delete_all", self)
        button_layout2.addWidget(self.select_all_btn)
        button_layout2.addWidget(self.delete_all_btn)
        main_layout.addLayout(button_layout2)

        
        output_label = QLabel("📜 Output:")
        output_label.setFont(QFont("Arial", 12, QFont.Bold))
        main_layout.addWidget(output_label)

        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 11))
        self.output.setPlaceholderText("Здесь будет вывод скрипта...")
        main_layout.addWidget(self.output, 2)

        self.setLayout(main_layout)

       
        self.save_btn.clicked.connect(self.save_file)
        self.new_file_btn.clicked.connect(self.new_file)
        self.run_btn.clicked.connect(self.run_script)
        self.select_all_btn.clicked.connect(self.select_all)
        self.delete_all_btn.clicked.connect(self.delete_all)
        self.theme_btn.clicked.connect(self.toggle_theme)

        
        if self.dark_mode:
            self.set_dark_theme()
        else:
            self.set_light_theme()

        self.show()

    
    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.Base, QColor(40, 40, 40))
        palette.setColor(QPalette.AlternateBase, QColor(60, 60, 60))
        palette.setColor(QPalette.Text, QColor(220, 220, 220))
        palette.setColor(QPalette.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
        palette.setColor(QPalette.Highlight, QColor(100, 150, 255))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        QApplication.instance().setPalette(palette)
        QApplication.instance().setStyleSheet("""
            QPushButton {
                background-color: #2e2e2e;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 6px 12px;
                color: #f0f0f0;
            }
            QPushButton:hover { background-color: #444; }
            QPushButton:pressed { background-color: #666; }
        """)
        self.theme_btn.setText("🌙 Dark")

    def set_light_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(245, 245, 245))
        palette.setColor(QPalette.WindowText, QColor(30, 30, 30))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(230, 230, 230))
        palette.setColor(QPalette.Text, QColor(30, 30, 30))
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, QColor(30, 30, 30))
        palette.setColor(QPalette.Highlight, QColor(50, 120, 200))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        QApplication.instance().setPalette(palette)
        QApplication.instance().setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #bbb;
                border-radius: 6px;
                padding: 6px 12px;
                color: #222;
            }
            QPushButton:hover { background-color: #ddd; }
            QPushButton:pressed { background-color: #ccc; }
        """)
        self.theme_btn.setText("☀️ Light")
        self.highlighter = PythonHighlighter(self.editor.document())

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.settings.setValue("dark_mode", self.dark_mode) 
        if self.dark_mode:
            self.set_dark_theme()
        else:
            self.set_light_theme()

    
    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "",
            "Текстовые файлы (*.txt *.py);;Все файлы (*)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.editor.toPlainText())
                QMessageBox.information(self, "Успех", f"Файл сохранён: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def new_file(self):
        self.editor.clear()
        self.output.clear()

  
    def run_script(self):
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True, text=True
        )
        self.output_console.setPlainText(
            f"=== ВЫВОД ===\n{result.stdout}\n\n=== ОШИБКИ ===\n{result.stderr}"
        )

        
        tmp_file = os.path.join(tempfile.gettempdir(), "eldos_tmp.py")
        with open(tmp_file, "w", encoding="utf-8") as f:
            f.write(code)

        self.output.clear()
        if self.process:
            self.process.kill()

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        self.process.start(sys.executable, [tmp_file])

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output.append(data)

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.output.append(f"<span style='color:red;'>{data}</span>")

    def process_finished(self):
        self.output.append("\n=== ✅ Процесс завершён ===")

    
    def select_all(self):
        self.editor.selectAll()

    def delete_all(self):
        self.editor.clear()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Program()
    sys.exit(app.exec_())
