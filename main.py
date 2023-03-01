import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5 import uic
from DMS import DatabaseManagementSystem
from PyQt5.QtGui import QTextDocument
from UI import mainForm

DB_NAME = "data/coffee.sqlite"
TITLE = "Coffee"


def raise_not_implemented_error() -> None:
    raise NotImplementedError


class MainWindow(mainForm.Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.dms = DatabaseManagementSystem(DB_NAME)
        self.current_coffee_cup_id = None
        ids = self.dms.get_ids()
        if ids:
            self.current_coffee_cup_id = min(ids)[0]
        self.total_amount_of_coffee_cups = len(ids)
        self.new_id = None
        self.init_ui()

    def init_ui(self) -> None:
        self.setFixedSize(self.size())
        self.setWindowTitle(TITLE)

        self.next.clicked.connect(self.next_coffee_cup)
        self.previous.clicked.connect(self.previous_coffee_cup)
        self.saveCoffeeCup.clicked.connect(self.save)
        self.deleteCoffeeCup.clicked.connect(self.delete)

        self.newCoffeeCup.clicked.connect(lambda: (self.menu.setCurrentIndex(1),
                                                   self.set_new_id(),
                                                   self.clear_editor()))
        self.edit.clicked.connect(lambda: (self.menu.setCurrentIndex(1), self.load_to_editor()))

        self.choose.clicked.connect(lambda: raise_not_implemented_error())
        self.like.clicked.connect(lambda: raise_not_implemented_error())
        self.small.clicked.connect(lambda: raise_not_implemented_error())
        self.medium.clicked.connect(lambda: raise_not_implemented_error())
        self.large.clicked.connect(lambda: raise_not_implemented_error())

        self.lightRoast.setChecked(True)
        self.ground.setChecked(True)
        self.smallSize.setChecked(True)

        self.load_coffee_cup()

    def set_new_id(self):
        grade_ids = self.dms.get_ids()
        for i in range(len(grade_ids)):
            if i != grade_ids[i][0] - 1:
                self.new_id = i + 1
                break
        else:
            self.new_id = len(grade_ids) + 1

    def next_coffee_cup(self) -> None:
        self.current_coffee_cup_id = (self.current_coffee_cup_id + 1) % self.total_amount_of_coffee_cups
        self.load_coffee_cup()

    def previous_coffee_cup(self) -> None:
        self.current_coffee_cup_id = (self.current_coffee_cup_id - 1) % self.total_amount_of_coffee_cups
        self.load_coffee_cup()

    def save(self):
        if self.new_id is None:
            return
        name = self.name.text()
        roast_level = [self.lightRoast.isChecked(), self.mediumRoast.isChecked(), self.darkRoast.isChecked()].index(
            True)
        gb = [self.ground.isChecked(), self.bean.isChecked()].index(True)
        if gb == 0:
            gb = (True, False)
        else:
            gb = (False, True)
        size = [self.smallSize.isChecked(), self.mediumSize.isChecked(), self.largeSize.isChecked()].index(True)
        description: QTextDocument = self.descriptionEditoer.document().toPlainText()
        self.dms.save_grade(self.new_id, name,
                            roast_level,
                            description,
                            *gb,
                            self.spinBox.value(),
                            size)
        self.load_coffee_cup()
        ids = self.dms.get_ids()
        self.total_amount_of_coffee_cups = len(ids)

    def delete(self):
        raise_not_implemented_error()

    def load_coffee_cup(self):
        data = self.dms.get_data_by_id(self.current_coffee_cup_id + 1)
        rst = {0: "Легкая", 1: "Средняя", 2: "Темная"}
        gb = {1: "Молотый", 0: "В зернах"}
        sz = {0: "Маленький", 1: "Средний", 2: "Большой"}
        s = f"""Название: {data[1]}
Тип обжарки: {rst[data[2]]}
Описание: {data[3]}
Тип: {gb[data[4]]}
Цена: {data[6]}
Размер: {sz[data[7]]}"""

        self.description.document().setPlainText(s)

    def load_to_editor(self):
        data = self.dms.get_data_by_id(self.current_coffee_cup_id + 1)
        self.name.setText(data[1])
        self.new_id = self.current_coffee_cup_id + 1
        if data[2] == 0:
            self.lightRoast.setChecked(True)
        elif data[2] == 1:
            self.mediumRoast.setChecked(True)
        elif data[2] == 2:
            self.darkRoast.setChecked(True)

        if data[4] == 0:
            self.ground.setChecked(True)
            self.bean.setChecked(False)
        else:
            self.ground.setChecked(False)
            self.bean.setChecked(True)
        self.descriptionEditoer.document().setPlainText(data[3])
        self.spinBox.setValue(data[5])
        if data[6] == 0:
            self.smallSize.setChecked(True)
        elif data[6] == 1:
            self.mediumSize.setChecked(True)
        elif data[6] == 2:
            self.largeSize.setChecked(True)

    def clear_editor(self):
        self.name.setText("")
        self.lightRoast.setChecked(True)
        self.ground.setChecked(True)
        self.descriptionEditoer.document().setPlainText("")
        self.spinBox.setValue(1)
        self.smallSize.setChecked(True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.excepthook = except_hook
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
