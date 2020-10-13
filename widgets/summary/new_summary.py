import tkinter as tk
import json
from functools import partial
from tkinter import ttk
from widgets.summary.summary_functions import fill_file


# Open the settings file
with open('settings.json') as json_file:
    settings = json.load(json_file)

# Open the data file
with open('widgets/summary/summary_data.json') as json_file:
    widgets_data = json.load(json_file)


class Summary:
    """ Widget that shows some label and data """

    def __init__(self, p_section_frame, p_widget_configuration_frame, p_widget_group, p_width, p_height):
        """
        Initialization of the summary widget that shows some label and data

        :param p_parent: Page that will contain this summary widget
        :param p_row: Row of the page where the widget will be placed
        :param p_widget_group: Group containing this widget
        """

        # Saving the parameters to use them in each function
        self.frame_section = p_section_frame
        self.widget_group = p_widget_group
        self.frame_widget_configuration = p_widget_configuration_frame

        # Add this widget to p_parent widgets
        self.widget_group.widgets.append(self)
        self.type = "Summary"

        # Properties of the widget-
        frame_height = p_height
        frame_width = p_width
        self.frame = tk.Frame(self.frame_section.frame, bg="white", highlightthickness=1)
        self.frame.grid_propagate(False)
        self.frame.config(highlightbackground="grey")
        self.frame.grid(row=0, column=0, sticky="news")
        self.frame.update_idletasks()  # to display good dimensions with .winfo_width()
        self.frame.columnconfigure((0, 1, 2, 3), weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure((1, 2), weight=4)

        # Title of the page
        self.title = tk.Label(self.frame,text="Sommaire", bg="#333333", fg="white", compound="c", borderwidth=1, relief="raised")
        self.title.grid(row=0, column=0, columnspan=5, sticky="nwe", ipadx=10, ipady=5)
        self.title.config(font=("Calibri bold", 12))

        # Creation of the buttons that display data
        self.nb_column = 1 #4
        self.nb_row = 1 #2
        self.buttons = [[tk.Button() for j in range(0, self.nb_column)] for i in range(0, self.nb_row)]
        self.button_width = int(frame_width/self.nb_column)
        self.button_height = int((frame_height/self.nb_row)/16)
        for i in range(0, self.nb_row):
            for j in range(0, self.nb_column):
                self.buttons[i][j] = tk.Button(self.frame, width=self.button_width, height=self.button_height, text=" ", fg="white")
                self.buttons[i][j].grid(row=i+1, column=j, padx=(5, 5), pady=(5, 5))
                self.buttons[i][j].config(font=("Calibri bold", 10))
                self.buttons[i][j]['command'] = partial(self.choose_data, i, j)

        # Loading and changing the content of the buttons
        self.load()

        # Fill the data file
        fill_file()

        # User interaction with the button
        self.frame.bind("<Button-1>", self.on_click)
        self.buttons[0][0].bind("<Button-1>", self.on_click)
        self.title.bind("<Button-1>", self.on_click)


    def choose_data(self, p_i, p_j):
        """
        Function that opens a window where the user can choose which data will be displayed

        :param p_i: Row of the button
        :param p_j: Column of the button
        """

        # Window handle
        login_window = tk.Toplevel(self.frame_section.frame)
        login_window.resizable(False, False)
        # login_window_width = settings['dimensions']['window_login_width']
        # login_window_height = settings['dimensions']['window_login_height']
        login_window_width = 550
        login_window_height = 220
        screen_width = self.frame_section.frame.winfo_screenwidth()
        screen_height = self.frame_section.frame.winfo_screenheight()
        x_cord = int((screen_width / 2) - (login_window_width / 2))
        y_cord = int((screen_height / 2) - (login_window_height / 2))
        login_window.geometry("{}x{}+{}+{}".format(login_window_width, login_window_height, x_cord, y_cord))
        login_window.columnconfigure((0, 1, 2), weight=1)

        # Title of the login window
        bg_identification = settings['colors']['bg_identification']
        label_login_title = tk.Label(login_window, text="Ajouter une donnée", bg=bg_identification, fg="white")
        label_login_title.grid(row=0, columnspan=3, sticky='new', pady=(0, 0))
        font_login_title = settings['font']['font_login_title']
        font_size_login_title = settings['font_size']['font_size_login_title']
        label_login_title.config(font=(font_login_title, font_size_login_title))

        # Label - Choose data to draw
        label_data = tk.Label(login_window, text="Choisir la donnée \n à afficher")
        label_data.grid(row=1, column=0, pady=20, sticky='n')
        font_add_label_data = settings['font']['font_login_username']
        font_size_add_label_data = settings['font_size']['font_size_login_username']
        label_data.config(font=(font_add_label_data, font_size_add_label_data))

        # Combobox - Choose data to draw
        list_data = []
        for x in widgets_data['data']:
            list_data.append(x)
        combo_data = ttk.Combobox(login_window, values=list_data)
        combo_data.current(0)
        combo_data.grid(row=2, column=0)

        # Label - Choose background color
        label_bg_color = tk.Label(login_window, text="Choisir la couleur \ndu fond")
        label_bg_color.grid(row=1, column=1, pady=20, sticky='n')
        font_add_label_color = settings['font']['font_login_password']
        font_size_add_label_color = settings['font_size']['font_size_login_password']
        label_bg_color.config(font=(font_add_label_color, font_size_add_label_color))

        # Combobox - Choose background color to draw
        list_color = [" ", "black", "white", "red", "orange", "blue", "yellow", "purple", "green", "white"]
        combo_bg_color = ttk.Combobox(login_window, values=list_color)
        combo_bg_color.current(0)
        combo_bg_color.grid(row=2, column=1)

        # Label - Choose color
        label_color = tk.Label(login_window, text="Choisir la couleur \n"
                                                  " de la donnée")
        label_color.grid(row=1, column=2, pady=20, sticky='n')
        font_add_label_color = settings['font']['font_login_password']
        font_size_add_label_color = settings['font_size']['font_size_login_password']
        label_color.config(font=(font_add_label_color, font_size_add_label_color))

        # Combobox - Choose frontground color to draw
        list_color = [" ", "black", "white", "red", "orange", "blue", "yellow", "purple", "green", "white"]
        combo_fg_color = ttk.Combobox(login_window, values=list_color)
        combo_fg_color.current(0)
        combo_fg_color.grid(row=2, column=2)

        # Button - Validation
        button_validate = tk.Button(login_window, text="Valider", width=30)
        button_validate.grid(row=3, columnspan=3, pady=(30, 0))
        button_validate['command'] = partial(self.change_button, p_i, p_j, combo_data, combo_bg_color, combo_fg_color)

    def change_button(self, p_row, p_column, p_combo_data, p_combo_bg_color, p_combo_fg_color):
        """
        Function that update the button in (p_row,p_column) with the content p_combo and p_combo_color

        :param p_row: Row of the button
        :param p_column: Column of the button
        :param p_combo_data: Name of the data
        :param p_combo_bg_color: Combo background color of the data
        :param p_combo_fg_color: Combo background color of the data
        """

        # Get the content of comboboxes
        data = p_combo_data.get()
        bg_color = p_combo_bg_color.get()
        fg_color = p_combo_fg_color.get()

        if data == ' ':
            data_text = data
        else:
            data_text = data + '\n' + str(widgets_data['data'][data])

        if bg_color == ' ':
            background_color = "SystemButtonFace"
        else:
            background_color = bg_color

        if fg_color == ' ':
            frontground_color = "black"
        else:
            frontground_color = fg_color

        # Replace the buttons text with the comboboxes content
        self.buttons[p_row][p_column]['text'] = data_text
        self.buttons[p_row][p_column]['bg'] = background_color
        self.buttons[p_row][p_column]['fg'] = frontground_color

        # Save the data
        self.save(p_row, p_column, data, background_color, frontground_color)

    def save(self, p_row, p_column, p_data, p_bg_color, p_fg_color):
        """
        Function that saves the content of each button

        :param p_row: Row of the button
        :param p_column: Column of the button
        :param p_data: Name of the data
        :param p_bg_color: Background color of the data
        :param p_fg_color: Frontground color of the data
        """

        # Build the texts that will be add to the saving file
        key = str(p_row) + ',' + str(p_column)
        value_data = {key: p_data}
        value_bg_color = {key: p_bg_color}
        value_fg_color = {key: p_fg_color}

        # Update the saving file (.json) with these data
        widgets_data['summary_data'].update(value_data)
        widgets_data['summary_bg_color'].update(value_bg_color)
        widgets_data['summary_fg_color'].update(value_fg_color)
        with open('widgets/summary/summary_data.json', 'w') as outfile:
            json.dump(widgets_data, outfile, indent=4)

    def load(self):
        """
        Function that loads the content of each button
        """

        # # Get all the data contain in the "summary section" of the saving file
        # for x in widgets_data['summary_data']:
        #     coord = x.split(',')
        #     row = int(coord[0])
        #     column = int(coord[1])
        #     data = widgets_data['summary_data'][x]
        #     bg_color = widgets_data['summary_bg_color'][x]
        #     fg_color = widgets_data['summary_fg_color'][x]
        #     if data == ' ':
        #         data_text = data
        #     else:
        #         data_text = data + '\n' + str(widgets_data['data'][data])
        #     self.buttons[row][column]['text'] = data_text
        #     self.buttons[row][column]['bg'] = bg_color
        #     self.buttons[row][column]['fg'] = fg_color

        self.buttons[0][0]['text'] = "test"
        self.buttons[0][0]['bg'] = "red"
        self.buttons[0][0]['fg'] = "white"

    def update(self):
        print("Update Summary")

    def hide(self):
        self.frame.grid_forget()

    def show(self):
        self.frame.grid(row=0, column=0, sticky="news")


    def on_click(self, e):
        """ Function called when the user click on this section """

        self.frame_section.on_click(e)

        # Label - Choose data to draw
        label_data = tk.Label(self.frame_widget_configuration, text="Donnée", bg="white")
        label_data.grid(row=1, sticky='nwe')
        font_add_label_data = settings['font']['font_login_username']
        font_size_add_label_data = settings['font_size']['font_size_login_username']
        label_data.config(font=(font_add_label_data, font_size_add_label_data))

        # Combobox - Choose data to draw
        list_data = []
        for x in widgets_data['data']:
            list_data.append(x)
        combo_data = ttk.Combobox(self.frame_widget_configuration, values=list_data)
        combo_data.current(0)
        combo_data.grid(row=2, pady=(0,10))

        # Label - Choose background color
        label_bg_color = tk.Label(self.frame_widget_configuration, text="Couleur du fond", bg="white")
        label_bg_color.grid(row=3, sticky='n')
        font_add_label_color = settings['font']['font_login_password']
        font_size_add_label_color = settings['font_size']['font_size_login_password']
        label_bg_color.config(font=(font_add_label_color, font_size_add_label_color))

        # Combobox - Choose background color to draw
        list_color = [" ", "black", "white", "red", "orange", "blue", "yellow", "purple", "green", "white"]
        combo_bg_color = ttk.Combobox(self.frame_widget_configuration, values=list_color)
        combo_bg_color.current(0)
        combo_bg_color.grid(row=4, pady=(0,10))

        # Label - Choose color
        label_color = tk.Label(self.frame_widget_configuration, text="Couleur de la donnée", bg="white")
        label_color.grid(row=5, sticky='n')
        font_add_label_color = settings['font']['font_login_password']
        font_size_add_label_color = settings['font_size']['font_size_login_password']
        label_color.config(font=(font_add_label_color, font_size_add_label_color))

        # Combobox - Choose frontground color to draw
        list_color = [" ", "black", "white", "red", "orange", "blue", "yellow", "purple", "green", "white"]
        combo_fg_color = ttk.Combobox(self.frame_widget_configuration, values=list_color)
        combo_fg_color.current(0)
        combo_fg_color.grid(row=6, pady=(0, 10))

        # Button - Validation
        button_validate = tk.Button(self.frame_widget_configuration, text="Valider", width=30)
        button_validate.grid(row=7, pady=(10, 0), padx=(10, 10))
        button_validate['command'] = partial(self.change_button, 0, 0, combo_data, combo_bg_color, combo_fg_color)

