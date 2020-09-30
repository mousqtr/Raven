import tkinter as tk
import json

from gui import FrameContent, ButtonLeftText, ButtonTopText, WidgetGroup, Section
from login import Login
from widgets.summary.summary import Summary
from widgets.filters.filters import Filters
from widgets.modifiers.modifiers import Modifiers
from widgets.table.table import Table
from widgets.donut_chart.donut_chart import DonutChart

# Open the settings file
with open('settings.json') as json_file:
    settings = json.load(json_file)

# Custom settings
window_width_initial = settings['dimensions']['window_width']
window_height_initial = settings['dimensions']['window_height']
top_menu_height_initial = settings['dimensions']['top_menu_height']
left_menu_width_initial = settings['dimensions']['left_menu_width']
left_menu_height_initial = window_height_initial

company_name = settings['company_name']
font_company_name = settings['font']['font_company_name']
font_size_company_name = settings['font_size']['font_size_company_name']

bg_company_name = settings['colors']['bg_company_name']
bg_top_menu = settings['colors']['bg_top_menu']
bg_left_menu = settings['colors']['bg_left_menu']
bg_connect = settings['colors']['bg_connect']


# Root initialization
root = tk.Tk()
root.title("Gestionnaire d'inventaire")
root.resizable(True, True)
root.minsize(700, 700)
window_icon = tk.PhotoImage(file="img/box.png")
root.iconphoto(False, window_icon)
root.grid_propagate(False)


# Window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width_initial/2))
y_cordinate = int((screen_height/2) - (window_height_initial/2))
root.geometry("{}x{}+{}+{}".format(window_width_initial, window_height_initial, x_cordinate, y_cordinate))

# Left menu
frame_left = tk.Frame(root, bg=bg_left_menu, width=left_menu_width_initial, height=left_menu_height_initial)
frame_left.grid_propagate(False)
frame_left.grid(row=0, column=0, sticky='new')
frame_left.columnconfigure(0, weight=1)

# Company title
label_company_title = tk.Label(frame_left, text=company_name, bg=bg_company_name, fg="white", height=2)
label_company_title.grid(row=0, sticky='new', pady=(0, 20))
label_company_title.config(font=(font_company_name, font_size_company_name))

# Right frame (right part of the window)
frame_right_width_initial = window_width_initial - left_menu_width_initial
frame_right = tk.Frame(root, bg="black", width=frame_right_width_initial, height=window_height_initial)
frame_right.grid_propagate(False)
frame_right.grid(row=0, column=1, sticky='n')
frame_right.columnconfigure(0, weight=1)

# Top menu (include in right_frame)
top_menu_width = window_width_initial - left_menu_width_initial
frame_top_menu = tk.Frame(frame_right, bg=bg_top_menu, width=top_menu_width, height=top_menu_height_initial)
frame_top_menu.grid_propagate(False)
frame_top_menu.grid(row=0, sticky='n')
frame_top_menu.columnconfigure(0, weight=1)

# # Initialization of right sub frames (include in right_frame)
# Frame_dashboard = FrameContent(frame_right, "Dashboard", "#e8e8e8")
# Frame_research = FrameContent(frame_right, "Recherche", "#e8e8e8")
# Frame_settings = FrameContent(frame_right, "Paramètres", "#e8e8e8")
# Frame_modification = FrameContent(frame_right, "Modification", "#e8e8e8")
# Frame_historic = FrameContent(frame_right, "Historique", "#e8e8e8")
# Frame_help = FrameContent(frame_right, "Aide", "#e8e8e8")
# Frame_dashboard.frame.lift()

# # Initialization of the left menu buttons (include in left_frame)
# Button_dashboard = ButtonLeftText("Dashboard", 1, frame_left, bg_left_menu, (0, 10), Frame_dashboard.frame.lift)
# Button_research = ButtonLeftText("Recherche", 2, frame_left, bg_left_menu, (0, 10), Frame_research.frame.lift)
# Button_modification = ButtonLeftText("Modification", 3, frame_left, bg_left_menu, (0, 10), Frame_modification.frame.lift)
# Button_historic = ButtonLeftText("Historique", 4, frame_left, bg_left_menu, (0, 10), Frame_historic.frame.lift)
# Button_help = ButtonLeftText("Aide", 5, frame_left, bg_left_menu, (340, 10), Frame_help.frame.lift)
# Button_settings = ButtonLeftText("Paramètres", 6, frame_left, bg_left_menu, (0, 0), Frame_settings.frame.lift)



# # Widget group
# Widget_group_1 = WidgetGroup(1)
# Widget_group_2 = WidgetGroup(2)
#
# # Widgets
# Widget_summary = Summary(Frame_dashboard, Widget_group_1, 1)
# Widget_donut_chart = DonutChart(Frame_dashboard, Widget_group_1, 2)
# Widget_research = Filters(Frame_research, Widget_group_1, 1)
# Widget_table_1 = Table(Frame_research, Widget_group_1, 2)
# Widget_modifier = Modifiers(Frame_modification, Widget_group_1, 1)
# Widget_table_2 = Table(Frame_modification, Widget_group_2, 2)




Frame_dashboard = FrameContent(frame_right, "Dashboard", "#e8e8e8")
Button_dashboard = ButtonLeftText("Dashboard", 1, frame_left, bg_left_menu, (0, 10), Frame_dashboard.frame.lift)

nb_row = 3 # max 5
nb_column = 4 # max 5

section_width = int(frame_right_width_initial/nb_column)
section_width2 = int(2*frame_right_width_initial/nb_column)
section_height = int(Frame_dashboard.frame["height"]/nb_row)

Sections = []
section_id = 0
for i in range(nb_row):
    for j in range(nb_column):
        section = Section(Frame_dashboard, i, j, 1, section_width, section_height, section_id)
        Sections.append(section)
        section_id += 1

# Initialization of the top menu buttons (include in frame_top_menu)
Window_login = Login(root)
Button_login = ButtonTopText("Se connecter", 2, frame_top_menu, bg_connect, Window_login.create_login_window)

# Detect the window resize
def window_resize(event):

    # Update width
    offset_width = root.winfo_width() - window_width_initial
    frame_right["width"] = frame_right_width_initial + offset_width
    frame_top_menu["width"] = frame_right_width_initial + offset_width
    Frame_dashboard.frame["width"] = frame_right_width_initial + offset_width
    for child in Frame_dashboard.childrens:
        child.frame["width"] = section_width + offset_width/nb_column

    # Update height
    frame_left["height"] = root.winfo_height()
    frame_right["height"] = root.winfo_height()
    Frame_dashboard.frame["height"] = root.winfo_height() - top_menu_height_initial
    for child in Frame_dashboard.childrens:
        child.frame["height"] = section_height + (root.winfo_height() - top_menu_height_initial) / nb_row





root.bind("<Configure>", window_resize)

# display_data()

# Launch the GUI
root.mainloop()
