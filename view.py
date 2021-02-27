# Importamos tkinter para utilizar como GUI
from tkinter import Tk, Frame, Label, Entry, Button, NW, CENTER, SE, messagebox, DISABLED


class View:
    def __init__(self):
        self.root = Tk()
        self.root.title("Stroop Test")
        self.root.geometry('800x600')
        self.root.resizable(0, 0)

        # Configuramos la pantalla inicial
        self.initial_screen = Frame(self.root)
        self.initial_screen.config(bg='lightblue')
        self.initial_screen_name_label = Label(
            self.initial_screen, text='Nombre')
        self.initial_screen_name_entry = Entry(
            self.initial_screen)
        self.initial_screen_age_label = Label(
            self.initial_screen, text='Edad')
        self.initial_screen_age_entry = Entry(self.initial_screen)
        self.initial_screen_email_label = Label(
            self.initial_screen, text='Email')
        self.initial_screen_email_entry = Entry(self.initial_screen)
        self.initial_screen_instructions_label = Label(
            self.initial_screen, text='Para realizar este test debe'
            'presionar en su teclado la flecha que corresponde\n'
            'a la palabra que figura en pantalla. \n Para Rojo presione ←, '
            'para Azul presione ↑, para Verde '
            'presione ↓ y para Amarillo presione →',
            font=('Candara', 12), bg='lightblue')
        self.initial_screen_start_button = Button(
            self.initial_screen, text='Comenzar')

        # Entradas con los datos del usuario
        self.initial_screen_name_entry.insert(0, '')
        self.initial_screen_age_entry.insert(0, '')
        self.initial_screen_email_entry.insert(0, '')

        # Configuramos la pantalla del test
        self.test_screen = Frame(self.root)
        self.test_screen.config(bg="black")
        self.test_screen_label = Label(
            self.test_screen, width=40,
            text="Presioná cualquier tecla\npara comenzar",
            font=("Calibri", 35), fg='white', bg='black')

        # Configuramos la pantalla de los resultados
        self.score_board = Frame(self.root)
        self.score_board.config(bg="lightblue")
        self.score_board_user_label = Label(self.score_board)
        self.score_board_user_result = Label(
            self.score_board)
        self.score_board_first_place = Label(
            self.score_board, text='1.')
        self.score_board_second_place = Label(
            self.score_board, text='2.')
        self.score_board_third_place = Label(
            self.score_board, text='3.')
        self.score_board_erase_button = Button(
            self.score_board, text='Borrar tu resultado')

        self.show_initial_screen()

        return

    def show_initial_screen(self):
        self.initial_screen.pack(side='top', fill='both', expand=True)
        self.initial_screen_name_label.pack(
            side='top', pady=50)
        self.initial_screen_name_entry.pack(side='top')
        self.initial_screen_age_label.pack(
            side='top', pady=40)
        self.initial_screen_age_entry.pack(side='top')
        self.initial_screen_email_label.pack(
            side='top', pady=40)
        self.initial_screen_email_entry.pack(side='top')
        self.initial_screen_start_button.pack(
            side='bottom', anchor=SE, padx=30, pady=40)
        self.initial_screen_instructions_label.pack(
            side='bottom', anchor=CENTER, pady=20)

        return

    def hide_initial_screen(self):
        # Nos sirve para que no aparezca ningún widget de la pantalla inicial
        self.initial_screen.pack_forget()
        return

    def change_from_initial_to_test_screen(self):
        # Cambiamos a la pantalla inicial a la pantalla del test
        self.hide_initial_screen()
        self.show_test_screen()
        return

    def show_error_message_pop_up(self, message):
        # Creamos una ventana de error
        messagebox.showerror('Error', message)
        return

    def show_test_screen(self):
        self.test_screen.pack(side='top', fill='both', expand=True)
        self.test_screen_label.pack(side='top', pady=250)
        self.test_screen.focus_set()
        return

    def hide_test_screen(self):
        self.test_screen.pack_forget()
        return

    def change_from_test_to_score_board(self):
        # Cambiamos de la pantalla del test a la pantalla de resultados
        self.hide_test_screen()
        self.show_score_board()
        return

    def show_score_board(self):
        self.score_board.pack(side='top', fill='both', expand=True)
        self.score_board_user_label.pack(side='top', anchor=NW, pady=50)
        self.score_board_user_result.pack(side='top')
        self.score_board_first_place.pack(side='top')
        self.score_board_second_place.pack(side='top')
        self.score_board_third_place.pack(side='top')
        self.score_board_erase_button.pack(side='bottom', pady=50)
        return

    def set_score_board_current_user_name(self, name):
        # Dato del nombre del usuario actual
        self.score_board_user_label.config(text='Nombre: ' + name)
        return

    def set_score_board_current_test_score(self, test_score):
        # Dato del último resultado del usuario actual
        self.score_board_user_result.config(
            text='Tu puntaje fue de: %.2f' % test_score)
        return

    def set_score_board_first_place_user(self, user):
        # Consultamos el primer lugar con nombre de usuario y resultado
        self.score_board_first_place.config(
            text='1. %s (%.2f)' % (user.name, user.average_score))
        return

    def set_score_board_second_place_user(self, user):
        # Consultamos el segundo lugar con nombre de usuario y resultado
        self.score_board_second_place.config(
            text='1. %s (%.2f)' % (user.name, user.average_score))
        return

    def set_score_board_third_place_user(self, user):
        # Consultamos el tercer lugar con nombre de usuario y resultado
        self.score_board_third_place.config(
            text='1. %s (%.2f)' % (user.name, user.average_score))
        return

    def disable_erase_button(self):
        # Desactivamos el botón Borrar los resultados una vez presionado
        self.score_board_erase_button.config(state=DISABLED)
        return

    def show_user_data_deleted_message(self):
        # Ventana emergente que corrobora que los datos fueron borrados
        messagebox.showinfo('OK', 'Datos borrados con éxito')
        return

    def start_gui(self):
        self.root.mainloop()
        return
