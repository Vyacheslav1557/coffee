GET_ALL_GRADES = """
SELECT *
  FROM grades
"""
GET_GRADES_IDS = """
SELECT id
  FROM grades;
"""
DELETE_FROM_GRADES_BY_ID = """
DELETE
  FROM grades
 WHERE id = ?;
"""
INSERT_INTO_GRADES = """
INSERT INTO grades VALUES(?, ?, ?, ?, ?, ?, ?, ?);
"""
SELECT_FROM_GRADES_BY_ID = """
SELECT *
  FROM grades
 WHERE id = ?;
"""
