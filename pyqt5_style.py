import sys, os, tempfile, keyword, re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QLabel
)
from PyQt5.QtCore import QProcess, Qt, QSettings
from PyQt5.QtGui import (
    QPalette, QColor, QFont, QIcon,
    QSyntaxHighlighter, QTextCharFormat
)


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#569CD6"))
        self.keyword_format.setFontWeight(QFont.Bold)

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#CE9178"))

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#6A9955"))
        self.comment_format.setFontItalic(True)

        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor("#B5CEA8"))

        self.rules = []
        keywords = keyword.kwlist + ["print"]
        for kw in keywords:
            pattern = r"\b" + kw + r"\b"
            self.rules.append((re.compile(pattern), self.keyword_format))

        self.rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), self.string_format))
        self.rules.append((re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), self.string_format))
        self.rules.append((re.compile(r"#.*"), self.comment_format))
        self.rules.append((re.compile(r"\b[0-9]+\b"), self.number_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)
