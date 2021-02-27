# Importamos el sistema de gestión de base de datos a utilizar: sqlite3
import sqlite3
import random
import datetime


class User():
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
        self.average_score = 0
        return


class Test():
    def __init__(self, user_name, start_timestamp):
        self.user_name = user_name
        self.start_timestamp = start_timestamp
        self.end_timestamp = None
        self.test_score = None
        return


class DatabaseManager():
    def __init__(self, db_filename):
        # Creamos la base de datos con su respectivas tablas
        self.db_filename = db_filename
        self.conn = sqlite3.connect(db_filename)
        self.conn.execute('PRAGMA foreign_keys=on;')

        self.create_tables()
        return

    # Cerramos la base de datos
    def close_db(self):
        self.conn.close()
        print('DB was closed!')
        return

    def create_tables(self):
        # Creamos la tabla Users
        self.conn.execute('''CREATE TABLE IF NOT EXISTS Users (
                                Name            TEXT    PRIMARY KEY NOT NULL,
                                Age             INT     NOT NULL,
                                Email           TEXT    NOT NULL,
                                AverageScore    REAL
        );''')

        # Creamos la tabla Tests
        self.conn.execute('''CREATE TABLE IF NOT EXISTS Tests (
                                UserName        TEXT    NOT NULL,
                                StartTimestamp  TEXT    NOT NULL,
                                EndTimestamp    TEXT    NOT NULL,
                                TestScore       REAL    NOT NULL,
                                FOREIGN KEY(UserName) REFERENCES Users(Name)
        );''')

        return

    def insert_user(self, name, age, email):
        # Damos de alta un nuevo usuario
        self.conn.execute(
            'INSERT INTO Users (Name, Age, Email) VALUES (?, ?, ?)',
            (name, age, email))
        self.conn.commit()
        return

    def delete_user(self, name):
        # Borramos un usuario
        self.conn.execute('DELETE FROM Users WHERE Name = ?', (name,))
        self.conn.commit()
        return

    def update_average_score(self, name, average_score):
        # Actualizamos los puntajes de un usuario
        print('update_average_score():', name, average_score)
        self.conn.execute(
            'UPDATE Users SET AverageScore = ? WHERE Name = ?',
            (average_score, name))
        self.conn.commit()
        return

    def delete_user_tests(self, name):
        # Borramos los test de un usuario para la tabla Tests
        self.conn.execute('DELETE FROM Tests WHERE UserName = ?', (name,))
        self.conn.commit()
        return

    def get_user(self, name):
        # Obtenemos los datos de un usuario
        cursor = self.conn.execute(
            'SELECT Name, Age, Email, AverageScore FROM Users WHERE Name = ?',
            (name,))
        db_user = cursor.fetchone()
        return db_user

    def add_test(self, name, start_timestamp, end_timestamp, test_score):
        # Añadimos un test
        self.conn.execute(
            'INSERT INTO Tests (UserName, StartTimestamp, EndTimestamp,'
            'TestScore) VALUES (?, ?, ?, ?)',
            (name, start_timestamp, end_timestamp, test_score))
        self.conn.commit()
        return

    def get_tests(self, name):
        # Obtenemos los datos de un test
        position = self.conn.execute(
            'SELECT UserName, StartTimestamp, EndTimestamp, '
            'TestScore FROM Tests WHERE UserName = ?', (name,))
        db_test = position.fetchall()
        return db_test

    def get_average_score_from_user(self, name):
        # Obtenemos el resultado promedio de un test
        cursor = self.conn.execute(
            'SELECT AVG(TestScore) FROM Tests WHERE UserName = ?', (name,))
        avg_score = cursor.fetchone()[0]
        return avg_score

    def get_top_three_score_users(self):
        # Obtenemos los tres mejores resultados de tests
        cursor = self.conn.execute(
            'SELECT Name, Age, Email, AverageScore FROM Users '
            'ORDER BY AverageScore DESC LIMIT 3')
        top_score_users = cursor.fetchall()
        return top_score_users


class Model:
    def __init__(self):
        # Originamos la base de datos
        self.db = DatabaseManager('stroop.db')

        self.current_user = None
        self.current_test = None
        self.current_test_results = []
        self.test_step = 0
        self.next_text = None
        self.next_color = None
        return

    def close_db(self):
        self.db.close_db()
        return

    def delete_all_current_user_data(self):
        self.db.delete_user_tests(self.current_user.name)
        self.db.delete_user(self.current_user.name)
        return

    def add_test(self, test_result):
        self.db.add_test(test_result.user_name, test_result.start_timestamp,
                         test_result.end_timestamp, test_result.test_score)
        return

    def set_current_user(self, name, age, email):
        self.current_user = User(name, age, email)
        db_user = self.db.get_user(name)
        if db_user is None:
            self.db.insert_user(name, age, email)
        return

    def start_new_test(self):
        start_timestamp = datetime.datetime.now()
        self.current_test = Test(self.current_user.name, start_timestamp)
        return

    def get_next_step_colors(self):
        # Definimos las variables a utilizar en el test y su uso
        colors_texts = ['Rojo', 'Azul', 'Verde', 'Amarillo']
        colors = ['red', 'blue', 'green', 'yellow']

        # Remove current colors from the colors list before choosing the next one
        if self.next_text in colors_texts:
            colors_texts.remove(self.next_text)
        if self.next_color in colors:
            colors.remove(self.next_color)

        self.next_text = random.choice(colors_texts)
        self.next_color = random.choice(colors)

        self.test_step += 1

        return [self.next_text, self.next_color]

    def check_step_result(self, pressed_key):
        # Corroboramos cuáles teclas fueron presionadas y si es correcto
        key_color_map = {'Left': 'Rojo', 'Up': 'Azul',
                         'Down': 'Verde', 'Right': 'Amarillo'}

        if self.test_step == 0:
            return

        if pressed_key in key_color_map:
            color_key_pressed = key_color_map[pressed_key]
        else:
            print('Wrong key pressed')
            return

        if color_key_pressed == self.next_text:
            print("\N{grinning face with smiling eyes} \u2705 \u2B50 Correct")
            self.current_test_results.append(1)
        else:
            print("\N{pouting face} \u2757 \u274C Incorrect")
            self.current_test_results.append(0)
        return

    def is_test_finished(self):
        # Una vez que el usuario hace 10 ejercicios finaliza el test
        if len(self.current_test_results) == 20:
            return True
        else:
            return False

    def end_test(self):
        # Agregar un nuevo test a la base de datos
        end_timestamp = datetime.datetime.now()
        self.current_test.end_timestamp = end_timestamp
        test_time = (self.current_test.end_timestamp -
                     self.current_test.start_timestamp).total_seconds()
        self.current_test.test_score = sum(
            self.current_test_results) / test_time

        self.db.add_test(self.current_test.user_name,
                         self.current_test.start_timestamp,
                         self.current_test.end_timestamp,
                         self.current_test.test_score)

        # Obtener un nuevo resultado promedio desde la tabla Test
        user_average_score = self.db.get_average_score_from_user(
            self.current_user.name)

        # Asignar el resultado en el usuario actual y guardarlo en la base
        self.current_user.average_score = user_average_score
        self.db.update_average_score(
            self.current_user.name, user_average_score)

        print('Test ended. Score:', self.current_test.test_score)
        return

    def get_top_three_score_users(self):
        # Obtener los tres mejores resultados de los usuarios
        top_score_users_db = self.db.get_top_three_score_users()
        top_score_users = []

        if len(top_score_users_db) > 0:
            user_db = top_score_users_db[0]
            user = User(user_db[0], user_db[1], user_db[2])
            user.average_score = user_db[3]
            top_score_users.append(user)
        else:
            top_score_users.append(None)

        if len(top_score_users_db) > 1:
            user_db = top_score_users_db[1]
            user = User(user_db[0], user_db[1], user_db[2])
            user.average_score = user_db[3]
            top_score_users.append(user)
        else:
            top_score_users.append(None)

        if len(top_score_users_db) > 2:
            user_db = top_score_users_db[2]
            user = User(user_db[0], user_db[1], user_db[2])
            user.average_score = user_db[3]
            top_score_users.append(user)
        else:
            top_score_users.append(None)

        return top_score_users


model = Model()
