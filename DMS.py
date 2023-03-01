import sqlite3
from queries import *


class DatabaseManagementSystem:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def get_ids(self) -> list:
        return self.cursor.execute(GET_GRADES_IDS).fetchall()

    def delete_by_id(self, grade_id):
        self.cursor.execute(DELETE_FROM_GRADES_BY_ID, (grade_id,))
        self.connection.commit()

    def get_all_grades(self) -> list:
        return self.cursor.execute(GET_ALL_GRADES).fetchall()

    def save_grade(self, *data) -> None:
        self.cursor.execute(DELETE_FROM_GRADES_BY_ID, (data[0],))
        self.cursor.execute(INSERT_INTO_GRADES, data)
        self.connection.commit()

    def get_data_by_id(self, grade_id) -> list:
        return self.cursor.execute(SELECT_FROM_GRADES_BY_ID, (grade_id,)).fetchone()
