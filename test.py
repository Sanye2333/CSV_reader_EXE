import sys
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QTextEdit,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt6.uic import loadUi

class MainWindow(QWidget):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        # 加载你设计的ui文件
        loadUi("ui_analyse.ui", self)
        self.setWindowTitle("CSV分析工具")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())