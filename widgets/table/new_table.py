import tkinter as tk
import pandas as pd
from functools import partial
import json
from tkinter import ttk

# Open the settings file
with open('settings.json') as json_file:
    settings = json.load(json_file)

# Open the data file
with open('widgets/table/table_data.json') as json_file:
    table_data = json.load(json_file)


class WidgetTable:
    """ Widget that displays a table """

    def __init__(self, p_section, p_widget_configuration_frame, p_widget_group):
        """
        Initialization of the table widget that shows a table

        :param p_parent: Page that will contain this table widget
        :param p_widget_group: Group containing this widget
        :param p_row: Row of the page where the widget will be placed
        """
        # Saving the parameters to use them in each function
        self.frame_section = p_section
        self.widget_group = p_widget_group
        self.widget_configuration = p_widget_configuration_frame
        self.frame_widget_configuration = p_widget_configuration_frame.frame

        self.frame_section_width = self.frame_section.frame.winfo_width()
        self.frame_section_height = self.frame_section.frame.winfo_height()


        # Initialization of the dataframe
        self.df = pd.read_csv('csv/csv_test.csv')
        self.nb_row_df = self.df.shape[0]
        self.nb_column_df = self.df.shape[1]
        self.list_rows = [i for i in range(0, self.nb_row_df)]

        # Initial values
        self.nb_column = 6
        self.nb_column_max = 6
        self.list_columns = [0, 1, 2, 3, 4, 5]

        
        self.list_width = [6 for i in range(6)]
        self.selected_row = -1

        # Add this widget to p_parent widgets
        self.widget_group.widgets.append(self)
        self.type = "Table"

        # Properties of the widget
        self.frame = tk.Frame(self.frame_section.frame, bg="green", highlightthickness=1)
        self.frame.grid_propagate(False)
        self.frame.config(highlightbackground="grey")
        self.frame.grid(sticky="news")
        self.frame.columnconfigure(0, weight=1)

        # Title - Table
        self.title = tk.Label(self.frame, text="Titre", bg="#333333", fg="white", compound="c", borderwidth=1, relief="raised")
        self.title.grid(row=0, sticky="nwes")
        self.title.config(font=("Calibri bold", 12))

        # Update these previous values with saving ones
        self.load()

        # Frame that contains headers of the table
        self.frame.update_idletasks()
        frame_header_width = self.frame.winfo_width() - 20
        self.frame_headers = tk.Frame(self.frame, bg="green", width=frame_header_width, height=20)
        self.frame_headers.grid(row=1, sticky="nws")
        self.frame_headers.update_idletasks()

        # Frame that will contain the table
        self.frame_canvas = tk.Frame(self.frame)
        self.frame_canvas.grid(row=2, sticky='nwes')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)
        self.frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        self.canvas = tk.Canvas(self.frame_canvas, bg="grey")
        self.canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.vsb = tk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # Objects specific to the table
        self.frame_buttons = tk.Frame(self.canvas, bg="grey")
        self.canvas.create_window((0, 0), window=self.frame_buttons, anchor='nw')
        self.buttons_header = [tk.Button() for j in range(self.nb_column)]
        self.buttons_table = [[tk.Button() for j in range(self.nb_column)] for i in range(self.nb_row_df)]

        # Boolean that indicates the creation of the table
        self.is_table_created = False

        # Creation of the table
        self.create_table(self.list_columns, self.list_rows)

        # User interaction with the button
        self.frame.bind("<Button-1>", self.on_click)
        self.title.bind("<Button-1>", self.on_click)
        self.frame.bind('<Configure>', self.resize)


    def create_table(self, p_list_col, p_list_rows):
        """
        Function that creates of the table

        :param p_nb_column: Number of column of the table
        :param p_width_column: Width of each column
        :param p_list_col: List which contains the column name of the table
        :param p_list_rows: List which contains the rows to draw
        """

        # Update values
        self.list_rows = p_list_rows
        self.list_columns = p_list_col
        nb_column = len(p_list_col)
        width_column = self.list_width[nb_column - 1]
        width_column1 = int(self.frame_headers.winfo_width()/nb_column)

        # Creation of the header
        self.frames_header = [tk.Frame() for j in range(nb_column)]
        self.buttons_header = [tk.Button() for j in range(nb_column)]
        current_col = 0
        for j in self.list_columns:
            self.frames_header[current_col] = tk.Frame(self.frame_headers, width=width_column1, height=20, bg="blue")
            self.frames_header[current_col].grid(row=0, column=current_col)
            self.frames_header[current_col].grid_propagate(False)
            self.frames_header[current_col].grid_columnconfigure(0, weight=1)
            self.frames_header[current_col].grid_rowconfigure(0, weight=1)

            self.buttons_header[current_col] = tk.Button(self.frames_header[current_col], text=list(self.df)[j-1])
            self.buttons_header[current_col].config(bg="green", fg="white")
            self.buttons_header[current_col].grid(row=0,column=0, sticky="news")
            # self.buttons_header[current_col].config(borderwidth=2, relief="ridge")
            current_col += 1

        # Creation of the table content
        self.frames_table = [[tk.Frame() for j in range(nb_column)] for i in range(self.nb_row_df)]
        self.buttons_table = [[tk.Button() for j in range(nb_column)] for i in range(self.nb_row_df)]


        current_col = 0
        current_row = len(self.list_rows)
        for j in self.list_columns:
            for i in range(0, self.nb_row_df):
                self.frames_table[i][current_col] = tk.Frame(self.frame_buttons, width=width_column1, height=20,
                                                           bg="blue")

                self.frames_table[i][current_col].grid_propagate(False)
                self.frames_table[i][current_col].grid_columnconfigure(0, weight=1)
                self.frames_table[i][current_col].grid_rowconfigure(0, weight=1)


                self.buttons_table[i][current_col] = tk.Button(self.frames_table[i][current_col], text=(self.df.iloc[i][j - 1]))
                self.buttons_table[i][current_col]['command'] = partial(self.color_line, i)
                self.buttons_table[i][current_col].config(borderwidth=2, relief="groove")

                if i in p_list_rows:

                    self.frames_table[i][current_col].grid(row=0, column=current_col)
                    self.frames_table[i][current_col].grid(row=self.list_rows.index(i), column=current_col)

                    self.buttons_table[i][current_col].config(fg="black")


                else:
                    self.frames_table[i][current_col].grid(row=current_row, column=current_col)
                    current_row += 1

                    self.buttons_table[i][current_col].config(state=tk.DISABLED, disabledforeground="SystemButtonFace")

                self.buttons_table[i][current_col].grid(row=0, column=0, sticky="news")

            current_row = len(self.list_rows)
            current_col += 1

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.frame_buttons.update_idletasks()

        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        first5columns_width = sum([self.buttons_table[0][j].winfo_width() for j in range(0, nb_column)])
        # first5rows_height = sum([self.buttons_table[i][0].winfo_height() for i in range(0, 16)])
        height = self.frame_section.frame.winfo_height() - 45
        self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                            height=height)

        # Set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Boolean that indicates the creation of the table
        self.is_table_created = True

    def on_click(self, e):
        """ Function called when the user click on this section """

        # Called the on_click function of its parent
        self.frame_section.on_click(e)

        self.frame_widget_configuration.grid_columnconfigure((0, 1), weight=1)

        # Modify the configuration widget title
        self.widget_configuration.label_title.grid(row=0, columnspan=2)

        # Label - Title
        label_title = tk.Label(self.frame_widget_configuration, text="Titre du widget", bg="#333333", fg="white")
        label_title.grid(row=1, columnspan=2, pady=(10, 0))
        label_title.config(font=("Calibri", 13))

        # Entry - Write the title
        self.entry_title = tk.Entry(self.frame_widget_configuration, width=15, textvariable=" ")
        self.entry_title.grid(row=2, columnspan=2)
        self.entry_title.config(font=("Calibri bold", 10))

        # Label - Choose columns
        label_select_column = tk.Label(self.frame_widget_configuration, text="Choix des colonnes", bg="#333333", fg="white")
        label_select_column.grid(row=3, columnspan=2, pady=(10, 0))
        label_select_column.config(font=("Calibri", 13))

        # Column choice label
        labels_column_choice = [tk.Label() for j in range(self.nb_column_max)]
        combo_column_choice = [ttk.Combobox() for j in range(self.nb_column_max)]
        list_headers = list(self.df.head())
        list_headers.insert(0, " ")
        for j in range(self.nb_column_max):
            label_text = "Colonne " + str(j + 1)
            labels_column_choice[j] = tk.Label(self.frame_widget_configuration, text=label_text, width=19, bg="#333333", fg="white")
            labels_column_choice[j].grid(row=j + 4, column=0, sticky='ne', padx=10, pady=1)
            labels_column_choice[j].config(font=("Calibri bold", 9))

            combo_column_choice[j] = ttk.Combobox(self.frame_widget_configuration, values=list_headers, state="readonly")
            combo_column_choice[j].grid(row=j + 4, column=1, sticky='nw', padx=10, pady=1)
            combo_column_choice[j].config(font=("Calibri bold", 9))
            combo_column_choice[j].current(0)

        # Button - Validation
        button_validate = tk.Button(self.frame_widget_configuration, text="Valider", width=19, bg="orange", fg="white")
        button_validate.grid(row=30, columnspan=2, pady=(20, 0))
        button_validate['command'] = partial(self.validate, combo_column_choice)
        button_validate.config(font=("Calibri", 10))

    def color_line(self, p_row):
        """
        Function that colors a line

        :param p_row: A line of the table
        """
        #Update values
        nb_column = len(self.list_columns)
        self.selected_row = p_row
        print(self.selected_row)

        for i in range(0, self.nb_row_df):
            for j in range(0, nb_column):
                if i == p_row:
                    self.buttons_table[i][j].config(bg="beige")
                else:
                    self.buttons_table[i][j].config(bg="SystemButtonFace")



    def details_window(self):
        """
        Functions called when the user clicks on details button
        """

        # Window handle
        window_details = tk.Toplevel(self.frame)
        window_details.resizable(False, False)
        window_details.title("Détails")
        window_icon = tk.PhotoImage(file="img/loupe.png")
        window_details.iconphoto(False, window_icon)
        # login_window_width = settings['dimensions']['window_login_width']
        # login_window_height = settings['dimensions']['window_login_height']
        window_settings_width = 550
        window_settings_height = 260
        screen_width = self.frame.winfo_screenwidth()
        screen_height = self.frame.winfo_screenheight()
        x_cord = int((screen_width / 2) - (window_settings_width / 2))
        y_cord = int((screen_height / 2) - (window_settings_height / 2))
        window_details.geometry("{}x{}+{}+{}".format(window_settings_width, window_settings_height, x_cord, y_cord))
        window_details.columnconfigure((0, 1), weight=1)

        # Title - Details
        bg_identification = settings['colors']['bg_identification']
        label_login_title = tk.Label(window_details, text="Détails", bg=bg_identification, fg="white")
        label_login_title.grid(row=0, columnspan=2, sticky='new', pady=(0, 10))
        font_login_title = settings['font']['font_login_title']
        font_size_login_title = settings['font_size']['font_size_login_title']
        label_login_title.config(font=(font_login_title, font_size_login_title))

        nb_column = len(self.list_columns)
        row_colored = 0
        for i in range(0, self.nb_row_df):
            for j in range(0, nb_column):
                if self.buttons_table[i][j]['bg'] == "beige":
                    row_colored = i

        # Label - Details
        labels_1 = [tk.Label() for j in range(self.nb_column_max)]
        labels_2 = [tk.Label() for j in range(self.nb_column_max)]
        list_headers = list(self.df.head())
        for j in range(self.nb_column_max):
            labels_1[j] = tk.Label(window_details, text=list_headers[j])
            labels_1[j].grid(row=j + 2, column=0, sticky='nw', padx=30, pady=1)
            labels_1[j].config(font=("Calibri bold", 10))
            labels_2[j] = tk.Label(window_details, text=self.df.loc[row_colored][j])
            labels_2[j].grid(row=j + 2, column=1, sticky='nw', padx=30, pady=1)
            labels_2[j].config(font=("Calibri bold", 10))

    def validate(self, p_combo):
        """
        Functions called when the user clicks on validate button - Change columns
        """

        # List of combobox indexes selected by the user
        list_columns = []
        for j in range(self.nb_column_max):
            col = p_combo[j].current()
            if (col != 0) and (col not in list_columns):
                list_columns.append(col)

        # offset
        for x in list_columns:
            x -= 1

        # sort columns in order
        list_columns.sort()

        # Replace columns with new ones
        number_col = len(list_columns)
        if number_col != 0:
            self.delete_buttons()
            self.create_table(list_columns, self.list_rows)


        # Save the columns state
        self.list_columns = list_columns
        # self.save(p_combo)

    def delete_buttons(self):
        """
        Functions that deletes headers and table buttons
        """

        # Destruction of the headers buttons
        for widget in self.frame_headers.winfo_children():
            widget.destroy()

        # Destruction of the headers buttons
        for widget in self.frame_buttons.winfo_children():
            widget.destroy()

    def resize(self, event):
        """ Function called when the parent section is resized"""

        print("Resize TableWidget")

        if self.is_table_created:

            # Get the number of column
            nb_column = len(self.list_columns)

            # Change frame_headers width
            frame_header_width = self.frame.winfo_width() - 20
            self.frame_headers.config(width=frame_header_width)

            # Calculate the new column width
            new_column_width = int(frame_header_width / nb_column)

            # Change frame_headers width
            current_col = 0
            for j in self.list_columns:
                self.frames_header[current_col].config(width=new_column_width)
                current_col += 1

            # Change the frame_table width
            current_col = 0
            for j in self.list_columns:
                for i in range(0, self.nb_row_df):
                    self.frames_table[i][current_col].config(width=new_column_width)
                current_col += 1

            # Change the canvas height
            frame_canvas_height = self.frame.winfo_height() - 45
            self.frame_canvas.config(height=frame_canvas_height)


    def hide(self):
        """ Hide the widget (during the edit widget mode)"""

        print("Hide ImageWidget")
        self.frame.grid_forget()

    def show(self):
        """ Hide the widget (after the edit widget mode)"""

        print("Show ImageWidget")
        self.frame.grid(row=0, column=0, sticky="news")

    def update(self):
        """
        Functions that create a new table with new rows
        """

        print("Update Table")

        # Delete the table
        self.delete_buttons()

        old_row = self.list_rows

        # Update the database
        self.df = pd.read_csv('csv/csv_test.csv')
        self.nb_row_df = self.df.shape[0]
        self.nb_column_df = self.df.shape[1]
        self.list_rows = [i for i in range(0, self.nb_row_df)]

        # # Update rows to draw
        rows = self.list_rows
        for w in self.widget_group.widgets:
            if w.type == "Filters":
                if w.row_to_draw == old_row or w.row_to_draw == []:
                    rows = self.list_rows
                else :
                    rows = w.row_to_draw

        # Recreate the table
        self.create_table(self.list_columns, rows)

    def save(self, p_combo):
        """
        Functions that saves the filters properties

        :param p_combo: Combobox with column choices
        """
        num_id = self.widget_group.id
        table_name = "table_" + str(num_id)
        table_data[table_name].update({"list_columns": self.list_columns})

        with open('widgets/table/table_data.json', 'w') as outfile:
            json.dump(table_data, outfile, indent=4)

    def load(self):
        """
        Function that loads the content of each filter
        """

        # Get all the data contain in the the saving file
        num_id = self.widget_group.id
        table_name = "table_" + str(num_id)
        self.list_columns = table_data[table_name]['list_columns']


