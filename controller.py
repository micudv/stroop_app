# Importamos model y view para administrar su funcionamiento en controller
import re
from view import View
from model import Model, User


class Controller:

    def __init__(self):
        self.view = View()
        self.view.initial_screen_start_button.config(
            command=self.start_test_button_pressed)
        self.view.test_screen.bind("<Key>", self.key_was_pressed)
        self.view.score_board_erase_button.config(
            command=self.erase_button_pressed)
        self.model = Model()

        self.view.root.protocol("WM_DELETE_WINDOW", self.close_app)
        return

    def close_app(self):
        self.model.close_db()
        self.view.root.destroy()
        return

    def start_test_button_pressed(self):
        # Obtenemos los datos ingresados desde View
        name = self.view.initial_screen_name_entry.get()
        age = self.view.initial_screen_age_entry.get()
        email = self.view.initial_screen_email_entry.get()

        print('introduced data:', name, age, email)

        # Validamos los datos
        try:
            self.validate_name(name)
            self.validate_age(age)
            self.validate_email(email)
        except Exception as e:
            # Si no son válidos, mostrar un mensaje de error
            self.view.show_error_message_pop_up(e)
            return

        self.model.set_current_user(name, age, email)

        # Si es válido, empezar un nuevo Test con User
        self.model.start_new_test()

        # Ocultamos la pantalla inicial y mostramos la pantalla del Test
        self.view.change_from_initial_to_test_screen()

        return

    # Utilizamos regex para validar los datos ingresados de Nombre, Edad, Email
    def validate_name(self, name):
        match = re.match("[a-zA-ZáéíóúñÁÉÍÓÚÑ ]", name)
        if match is None:
            raise Exception('Nombre no válido')
        return

    def validate_age(self, age):
        match = re.match("[0-9]", age)
        if match is None:
            raise Exception('Edad no válida')
        if int(age) < 10 or int(age) > 120:
            raise Exception('Edad fuera de rango')
        return

    def validate_email(self, email):
        match = re.match(r"(<)?(\w+@\w+(?:\.[a-z]+)+)(?(1)>|$)", email.lower())
        if match is None:
            raise Exception('Email no válido')
        return

    def key_was_pressed(self, event):
        print(event.keysym, "was pressed")

        self.model.check_step_result(event.keysym)

        test_is_finished = self.model.is_test_finished()
        if test_is_finished:
            self.model.end_test()
            # Si el Test finalizó, ocultar y mostrar la pantalla de Resultados
            self.view.change_from_test_to_score_board()
            self.view.set_score_board_current_user_name(
                self.model.current_user.name)
            self.view.set_score_board_current_test_score(
                self.model.current_test.test_score)

            top_score_users = self.model.get_top_three_score_users()
            if top_score_users[0] is not None:
                self.view.set_score_board_first_place_user(top_score_users[0])
            if top_score_users[1] is not None:
                self.view.set_score_board_second_place_user(top_score_users[1])
            if top_score_users[2] is not None:
                self.view.set_score_board_third_place_user(top_score_users[2])

        else:
            # Generar colores al azar paar el siguiente paso
            next_text, next_color = self.model.get_next_step_colors()
            self.view.test_screen_label.config(text=next_text, fg=next_color)

        return

    def erase_button_pressed(self):
        # Permite borrar de la base de datos los datos obtenidos de un usuario
        self.model.delete_all_current_user_data()
        self.view.disable_erase_button()
        self.view.show_user_data_deleted_message()
        return

    def start_app(self):
        self.view.start_gui()
        return


if __name__ == '__main__':
    controller = Controller()
    controller.start_app()
