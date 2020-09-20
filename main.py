import tkinter as tk
from functools import partial
import sqlite3
import pandas as pd
from product import Product
from tools import FrameRight, ButtonLeftText


# Custom settings
color_title = "#602320"
color_window = "#979aaa"
color_headers = "#eb8c00"
color_left_menu = "#333333"
window_width = 1000
window_height = 700
title_font = ("Calibri bold", 16)
menu_font = ("Calibri bold", 14)
low_font = ("Calibri bold", 13)
username_font = ("Calibri", 13)

# Root initialization
root = tk.Tk()
root.title("Gestionnaire d'inventaire")
root.resizable(True, True)
root.config(bg=color_window)
window_icon = tk.PhotoImage(file="inventory.png")
root.iconphoto(False, window_icon)

# Window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

# Window grid
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Left menu
frame_left_width = window_width/5
frame_left = tk.Frame(root, bg=color_left_menu, width=frame_left_width)
frame_left.grid(row=0, column=0, sticky='news')
frame_left.columnconfigure(0, weight=1)






# Left title
label_title = tk.Label(frame_left, text="Nom entreprise", bg="black", fg="white", height=2)
label_title.grid(row=0, sticky='new', pady=(0, 20))
label_title.config(font=title_font)





# Initialization of the left buttons
Button_dashboard = ButtonLeftText("Dashboard", 1, frame_left, color_left_menu, (0, 10), None)
Button_user = ButtonLeftText("Utilisateurs", 2, frame_left, color_left_menu, (0, 10), None)
Button_action = ButtonLeftText("Actions", 3, frame_left, color_left_menu, (0, 10), None)

frame_bottom_left = tk.Frame(frame_left, bg="#13547a", height=200, width=frame_left_width)
frame_bottom_left.grid(row=4, sticky='new', pady=(345, 0))
frame_bottom_left.columnconfigure(0, weight=1)

Button_help = ButtonLeftText("Aide", 0, frame_bottom_left, "#13547a", (10, 10), None)


def create_login_window():
    """ Creation of the login window """

    # Window handle
    login_window = tk.Toplevel(root)
    login_window_width = 500
    login_window_height = 250
    x_cord = int((screen_width / 2) - (login_window_width / 2))
    y_cord = int((screen_height / 2) - (login_window_height / 2))
    login_window.geometry("{}x{}+{}+{}".format(login_window_width, login_window_height, x_cord, y_cord))
    login_window.columnconfigure(0, weight=1)

    # Title of the login window
    label_login_title = tk.Label(login_window, text="Identification", bg="#13547a", fg="white")
    label_login_title.grid(row=0, sticky='new', pady=(0, 20))
    label_login_title.config(font=menu_font)

    # Username label
    label_username = tk.Label(login_window, text="Username")
    label_username.grid(row=1, sticky='new', pady=(0, 10))
    label_username.config(font=username_font)

    # Username entry
    var_username = tk.StringVar(value='')
    entry_username = tk.Entry(login_window, bg="white", width=30, textvariable=var_username, font=("Consolas", 15))
    entry_username.grid(row=2,  pady=(0, 20))

    # Password label
    label_password = tk.Label(login_window, text="Password")
    label_password.grid(row=3, sticky='new', pady=(0, 10))
    label_password.config(font=username_font)

    # Password entry
    var_password = tk.StringVar(value='')
    entry_password = tk.Entry(login_window, bg="white", width=30, textvariable=var_password, font=("Consolas", 15))
    entry_password.grid(row=4,  pady=(0, 20))

Button_6 = ButtonLeftText("Se connecter", 2, frame_bottom_left, "orange", (0, 0), create_login_window)

DashboardFrame = FrameRight(root, "Dashboard", "#e8e8e8")

# First frame
frame_first = tk.Frame(DashboardFrame.frame, bg="white", width=DashboardFrame.frame_width, height=200, highlightthickness=1)
frame_first.config(highlightbackground="grey")
frame_first.grid(row=1, sticky='new', padx=(10, 10), pady=(5, 10))
frame_first.columnconfigure(0, weight=1)

# Second frame
frame_second = tk.Frame(DashboardFrame.frame, bg="white", width=DashboardFrame.frame_width, height=200, highlightthickness=1)
frame_second.config(highlightbackground="grey")
frame_second.grid(row=2, sticky='new', padx=(10, 10), pady=(5, 10))
frame_second.columnconfigure(0, weight=1)


SettingsFrame = FrameRight(root, "Paramètres", "orange")

DashboardFrame.frame.lift()
Button_5 = ButtonLeftText("Paramètres", 1, frame_bottom_left, "#13547a", (0, 10), SettingsFrame.frame.lift)



# Launch the GUI
root.mainloop()
