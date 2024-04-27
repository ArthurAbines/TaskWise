import sqlite3
from User import User
from Task import Task


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    first_name TEXT,
                                    last_name TEXT,
                                    student_number TEXT PRIMARY KEY,
                                    username TEXT,
                                    password TEXT
                                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    task_name TEXT,
                                    task_desc TEXT,
                                    date TEXT,
                                    time TEXT,
                                    task_sub TEXT,
                                    task_cat TEXT,
                                    status TEXT,
                                    student_number TEXT,
                                    FOREIGN KEY (student_number) REFERENCES users(student_number)
                                )''')
        self.conn.commit()

    def save_user(self, user):
        self.cursor.execute('''INSERT INTO users VALUES (?, ?, ?, ?, ?)''',
                            (user.first_name, user.last_name, user.student_number, user.username, user.password))
        self.conn.commit()

    def load_users(self):
        self.cursor.execute('''SELECT * FROM users''')
        rows = self.cursor.fetchall()
        users = []
        for row in rows:
            user = User(row[0], row[1], row[2], row[3], row[4])
            users.append(user)
        return users

    def save_task(self, task, student_number):
        self.cursor.execute('''INSERT INTO tasks VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (task.task_name, task.task_desc, task.date, task.time, task.task_sub, task.task_cat, task.status, student_number))
        self.conn.commit()

    def update_task(self, task, student_number):
        self.cursor.execute('''UPDATE tasks SET task_name=?, task_desc=?, date=?, time=?, task_sub=?, task_cat=?, status=? WHERE task_id=? AND student_number=?''',
                            (task.task_name, task.task_desc, task.date, task.time, task.task_sub, task.task_cat, task.status, task.task_id, student_number))
        self.conn.commit()

    def delete_task(self, task, student_number):
        self.cursor.execute('''DELETE FROM tasks WHERE task_id=? AND student_number=?''', (task.task_id, student_number))
        self.conn.commit()

    def search_tasks(self, student_number, keyword):
        self.cursor.execute('''SELECT * FROM tasks WHERE student_number=? AND (task_id LIKE ? OR task_name LIKE ? OR task_desc LIKE ? OR task_sub LIKE ? OR task_cat LIKE ? OR status LIKE ?)''',
                            (student_number, f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        rows = self.cursor.fetchall()
        tasks = []
        for row in rows:
            task = Task(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            tasks.append(task)
        return tasks

    def update_task_status(self, task_id, new_status, student_number):
        self.cursor.execute('''UPDATE tasks SET status=? WHERE task_id=? AND student_number=?''',
                            (new_status, task_id, student_number))
        self.conn.commit()

    def load_tasks(self, student_number):
        self.cursor.execute('''SELECT * FROM tasks WHERE student_number = ?''', (student_number,))
        rows = self.cursor.fetchall()
        tasks = []
        for row in rows:
            task = Task(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            tasks.append(task)
        return tasks

    def close(self):
        self.conn.close()
