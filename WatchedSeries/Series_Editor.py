import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

DB_NAME = "DB/series.db"


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/UI_Mainwindow.ui", self)
        self.con = sqlite3.connect(DB_NAME)
        self.update_result()
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.edit_series)
        self.pushButton_3.clicked.connect(self.delete_series)
        self.pushButton_4.clicked.connect(self.add_series)
        self.modified = {}
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        query = "SELECT * FROM series ORDER BY id"
        result = cur.execute(query).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Ссылка', 'Жанр', 'Количество серий', 'Просмотрено'])
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()


    def add_series(self):
        dialog = AddSeriesWidget(self)
        dialog.show()

    def edit_series(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if not ids:
            self.statusBar().showMessage('Ничего не выбрано')
            return
        else:
            self.statusBar().showMessage('')
        dialog = AddSeriesWidget(self, series_id=ids[0])
        dialog.show()

    def delete_series(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы с id " + ",".join(ids),
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute("DELETE FROM series WHERE id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)
            self.con.commit()
            self.update_result()


class AddSeriesWidget(QMainWindow):
    def __init__(self, parent=None, series_id=None):
        super().__init__(parent)
        self.con = sqlite3.connect(DB_NAME)
        self.params = {}
        uic.loadUi('UI/UI_AddSeries.ui', self)
        self.series_id = series_id
        if series_id is not None:
            self.pushButton.clicked.connect(self.edit_elem)
            self.pushButton.setText('Отредактировать')
            self.setWindowTitle('Редактирование записи')
            self.get_elem()

        else:
            self.pushButton.clicked.connect(self.add_elem)

    def get_elem(self):
        cur = self.con.cursor()
        item = cur.execute(
            f"SELECT s.ID, s.Title, s.Link, s.Genre, s.NumOfSeries, s.Watched FROM series as s").fetchone()
        self.Title.setPlainText(item[1])
        self.Link.setPlainText(str(item[2]))
        self.Genre.setPlainText(str(item[3]))
        self.NumOfSeries.setPlainText(str(item[4]))
        self.Watched.setCheckState(bool(item[5]))


    def add_elem(self):
        cur = self.con.cursor()
        try:
            id_off = cur.execute("SELECT max(id) FROM series").fetchone()[0]
            new_data = (id_off + 1, self.Title.toPlainText(), self.Link.toPlainText(), self.Genre.toPlainText(),
                        int(self.NumOfSeries.toPlainText()), self.Watched.checkState())
            cur.execute("INSERT INTO series VALUES (?,?,?,?,?,?)", new_data)
        except ValueError as ve:
            self.statusBar().showMessage("Неверно заполнена форма")
            print(ve)
        else:
            self.con.commit()
            self.parent().update_result()
            self.close()

    def edit_elem(self):
        cur = self.con.cursor()
        try:
            new_data = (self.Title.toPlainText(), self.Link.toPlainText(), self.Genre.toPlainText(),
                        int(self.NumOfSeries.toPlainText()), self.Watched.checkState(), self.series_id)
            cur.execute("UPDATE series SET Title=?, Link=?, Genre=?, NumOfSeries=?, Watched=? WHERE id=?", new_data)
        except ValueError as ve:
            self.statusBar().showMessage("Неверно заполнена форма")
            print(ve)
        else:
            self.con.commit()
            self.parent().update_result()
            self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
