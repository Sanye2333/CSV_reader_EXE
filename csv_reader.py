import sys
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QTextEdit,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QTableWidgetItem
import matplotlib
matplotlib.use('Qt5Agg')
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class MainWindow(QWidget):
    """
    主窗口类
    """
    df_list = []
    clean_enabled = False
    overview_win = None
    def __init__(self):
        super().__init__()
        # 加载你设计的ui文件
        loadUi("ui_home.ui", self)
        self.setWindowTitle("CSV分析工具")
        self.btn_add_files.clicked.connect(self.add_files)
        self.btn_remove_selected.clicked.connect(self.remove_selected)
        self.btn_export_file.clicked.connect(self.export_file)
        self.btn_clean.clicked.connect(self.clean)
        self.btn_go_to_overview.clicked.connect(self.go_to_overview)
    
    def add_files(self):
        file,_=QFileDialog.getOpenFileName(self,"选择文件","","表格文件 (*.csv *.xlsx)")
        if file:
            self.listWidget_files.addItem(file)
            if file.endswith(".csv"):
                df = pd.read_csv(file)
                self.df_list.append(df)
            elif file.endswith(".xlsx"):
                df = pd.read_excel(file)
                self.df_list.append(df)
            else:
                QMessageBox.warning(self,"错误","不支持的文件格式")

    def remove_selected(self):
        current_row = self.listWidget_files.currentRow()
        if current_row >= 0:
            self.listWidget_files.takeItem(current_row)
            del self.df_list[current_row]

    def export_file(self):
        file,filetype=QFileDialog.getSaveFileName(self,"保存文件","","CSV 文件 (*.csv);;Excel 文件 (*.xlsx)")
        if file:
            if len(self.df_list) == 0:
                QMessageBox.warning(self,"错误","请先添加文件")
                return
            df_total = pd.concat(self.df_list, ignore_index=True)
            if self.clean_enabled:
                df_total = df_total.drop_duplicates()
                df_total = df_total.dropna()
            if filetype == "CSV 文件 (*.csv)":
                df_total.to_csv(file, index=False)
            elif filetype == "Excel 文件 (*.xlsx)":
                df_total.to_excel(file, index=False)
            QMessageBox.information(self,"成功","文件已保存")

    def clean(self):
        self.clean_enabled = not self.clean_enabled
        if self.clean_enabled==False:
            self.btn_clean.setText("数据清洗:关闭") 
            self.btn_clean.setStyleSheet("color: red;")
        else:
            self.btn_clean.setText("数据清洗:开启")
            self.btn_clean.setStyleSheet("color: green;")

    def go_to_overview(self):
        if len(self.df_list) == 0:
            QMessageBox.warning(self,"错误","请先添加文件")
            return
        df_total = pd.concat(self.df_list, ignore_index=True)
        if self.clean_enabled:
            df_total = df_total.drop_duplicates()
            df_total = df_total.dropna()
        self.overview_win = OverviewWindow(df_total,self)
        self.overview_win.show()
        self.hide()


class OverviewWindow(QWidget):
    """
    数据概览窗口类
    """
    df = None
    info_text = ""
    main_window = None
    def __init__(self, df,main_window):
        super().__init__()
        loadUi("ui_overview.ui", self)
        self.df = df
        self.main_window = main_window
        self.setWindowTitle("数据概览")
        self.info_text += "【数据基本信息】\n"
        self.info_text += f"总行数：{len(self.df)}\n"
        self.info_text += f"总列数：{len(self.df.columns)}\n\n"
        for col in self.df.columns:
            self.info_text += f"【{col}】\n"
            self.info_text += f"数据类型：{self.df[col].dtype}\n"
            self.info_text += f"缺失值数量：{self.df[col].isnull().sum()}\n"
            self.info_text += f"唯一值数量：{self.df[col].nunique()}\n"
            if df[col].dtype == "int" or df[col].dtype == "float":
                self.info_text += f"最小值：{self.df[col].min()}\n"
                self.info_text += f"最大值：{self.df[col].max()}\n"
                self.info_text += f"平均值：{self.df[col].mean()}\n"
                self.info_text += f"中位数：{self.df[col].median()}\n"
        self.text_info.setText(self.info_text)

        self.table_preview.clear()
        self.table_preview.setRowCount(0)
        rows = min(20, len(self.df))  # 最多显示20行
        cols = len(self.df.columns)
        self.table_preview.setRowCount(rows)
        self.table_preview.setColumnCount(cols)
        self.table_preview.setHorizontalHeaderLabels(self.df.columns)
        for row in range(rows):
            for col in range(cols):
                value = self.df.iloc[row, col]
                item = QTableWidgetItem(str(value))
                self.table_preview.setItem(row, col, item)

        self.combo_column_choose.clear()
        self.combo_column_choose.addItems(self.df.columns)
        self.btn_back_home.clicked.connect(self.back_home)
        self.btn_to_analyse.clicked.connect(self.to_analyse)
    
    def back_home(self):
        self.close()
        self.main_window.show()

    def to_analyse(self):
        col = self.combo_column_choose.currentText()
        if col == "":
            QMessageBox.warning(self,"错误","请选择列")
            return
        if self.df is None or self.df.empty:
            QMessageBox.warning(self,"错误","数据表为空")
            return
        if col not in self.df.columns:
            QMessageBox.warning(self,"错误","列不存在")
            return
        if self.df[col].isnull().all():
            QMessageBox.warning(self,"错误","该列全为空数据")
            return
        if self.df[col].isnull().any():
            QMessageBox.warning(self,"错误","该列包含空值/NAN")
            return
        self.close()
        self.analyse_win = AnalyseWindow(self.df,col,self.main_window,self)
        self.analyse_win.show()


class AnalyseWindow(QWidget):
    df = None
    col = None
    main_window = None
    overview_window = None
    info_text = ""
    
    def __init__(self, df, col, main_window, overview_window):
        super().__init__()
        loadUi("ui_analyse.ui", self)
        self.setWindowTitle("单列分析")
        self.df = df
        self.col = col
        self.main_window = main_window
        self.overview_window = overview_window

        self.info_text += f"【{col}】\n"
        self.info_text += f"数据类型：{self.df[col].dtype}\n"
        self.info_text += f"缺失值数量：{self.df[col].isnull().sum()}\n"
        self.info_text += f"唯一值数量：{self.df[col].nunique()}\n"
        
        if df[col].dtype == "int" or df[col].dtype == "float":
            self.info_text += f"最小值：{self.df[col].min()}\n"
            self.info_text += f"最大值：{self.df[col].max()}\n"
            self.info_text += f"平均值：{self.df[col].mean()}\n"
            self.info_text += f"中位数：{self.df[col].median()}\n"

        cur_group = self.df.groupby(col)
        result = cur_group.agg({
            "open": "mean",
            "high": "mean",
            "low": "mean",
            "close": "mean",
            "volume": "sum"
        })
        self.info_text += "\n分组统计:\n"
        self.info_text += str(result.round(2))
        self.result = result

        self.init_plot()
        self.draw_plot()

        self.text_analysis_result.setText(self.info_text)
        self.btn_back_overview.clicked.connect(self.back_overview)
        self.btn_back_home.clicked.connect(self.back_home)

    def back_home(self):
        plt.close('all')
        self.close()
        self.main_window.show()
        
    def back_overview(self):
        plt.close('all')
        self.close()
        self.overview_window.show()

    def init_plot(self):
        self.fig = plt.figure(figsize=(12,8))
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout_plot.addWidget(self.toolbar)
        self.layout_plot.addWidget(self.canvas)

    def draw_plot(self):
        self.fig.clear()
        data = self.df[self.col].dropna()

        ax1 = self.fig.add_subplot(2,2,1)
        data.plot(kind='bar', ax=ax1)
        ax1.set_title(f'{self.col} - 分布')
        ax1.tick_params(axis='x',rotation=45,labelsize=8)

        ax2 = self.fig.add_subplot(2,2,2)
        data.plot(kind='line', ax=ax2)
        ax2.set_title(f'{self.col} - 趋势')

        ax3 = self.fig.add_subplot(2,2,3)
        data.plot(kind='hist', ax=ax3)
        ax3.set_title(f'{self.col} - 直方图')

        ax4 = self.fig.add_subplot(2,2,4)
        num_df = self.df.select_dtypes(include=['int64','float64'])
        if self.col in num_df.columns:
            corr = num_df.corr()
            im = ax4.imshow(corr, cmap='coolwarm')
            ax4.set_xticks(range(len(corr.columns)))
            ax4.set_yticks(range(len(corr.columns)))
            ax4.set_xticklabels(corr.columns, rotation=45)
            ax4.set_yticklabels(corr.columns)
            ax4.set_title('数值列相关性')

        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())