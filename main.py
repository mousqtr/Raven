import tkinter as tk
from functools import partial

from gui import MainWindow, LeftFrame, RightFrame, TopFrame, ButtonLeftText, ButtonTopText, MiddleFrame
from new_page import NewPage
from edit_page import EditPage
from login import Login
from widgets.summary.summary import Summary
from widgets.filters.filters import Filters
from widgets.modifiers.modifiers import Modifiers
from widgets.table.table import Table
from widgets.donut_chart.donut_chart import DonutChart


# Main window initialization
main_window = MainWindow()

# Images used in the left static frame (color 1/2)
img_pages = tk.PhotoImage(file="img/pages2.png")
img_widgets = tk.PhotoImage(file="img/widgets2.png")
img_settings = tk.PhotoImage(file="img/setting2.png")

# Images used in the left static frame (color 2/2)
img_pages2 = tk.PhotoImage(file="img/pages3.png")
img_widgets2 = tk.PhotoImage(file="img/widgets3.png")
img_settings2 = tk.PhotoImage(file="img/setting3.png")

# Images used as widgets icons
img_summary = tk.PhotoImage(file="img/widgets/summary.png")
img_graph = tk.PhotoImage(file="img/widgets/graph.png")
img_donut_chart = tk.PhotoImage(file="img/widgets/donut_chart.png")
img_histogram = tk.PhotoImage(file="img/widgets/histogram.png")
img_table = tk.PhotoImage(file="img/widgets/table.png")
img_histogram_graph = tk.PhotoImage(file="img/widgets/histogram_graph.png")
img_map = tk.PhotoImage(file="img/widgets/map.png")

# Images used in configuration mode
img_add = tk.PhotoImage(file="img/add.png")
img_delete = tk.PhotoImage(file="img/minus.png")
img_empty = tk.PhotoImage(file="img/empty.png")

# List containing theses images
list_img_1 = [img_pages, img_widgets, img_settings]
list_img_2 = [img_pages2, img_widgets2, img_settings2]
list_img_widgets = [img_summary, img_donut_chart, img_table, img_map, img_graph, img_histogram, img_histogram_graph]
list_buttons_widget = [img_add, img_delete, img_empty]

# List containing the names of each widget
list_title_widgets = ["Sommaire", "Graphique\nen anneau", "Table", "Carte", "Graphique", "Histogramme", "Graphe\nHistogramme"]

# Logo of the company
img_logo = tk.PhotoImage(file="img/logo.png")

# Creation of each frame of the window
frame_top = TopFrame(main_window, img_logo)
frame_middle = MiddleFrame(main_window)
frame_left = LeftFrame(frame_middle, frame_top, list_img_1, list_img_2)
frame_right = RightFrame(frame_middle, frame_left)


# Initialization of the widget button
def edit_widgets_mode(p_right_frame, p_list_img_widgets, p_list_title_widgets, p_list_buttons_widget):
    if len(frame_right.frames_content) > 0:
        frame_content_id = p_right_frame.current_frame
        frame_content = p_right_frame.frames_content[frame_content_id]
        frame_content.edit_widgets(p_list_img_widgets, p_list_title_widgets, p_list_buttons_widget)


button_configure_widgets = ButtonTopText("Configurer les widgets", 1, frame_top.third_top_frame,
                                         partial(edit_widgets_mode, frame_right, list_img_widgets, list_title_widgets, list_buttons_widget))

# Initialization of the login button
window_login = Login(main_window.frame)
button_login = ButtonTopText("Se connecter", 2, frame_top.third_top_frame, window_login.create_login_window)


# Initialization of the edit button
def edit_page():
    if len(frame_right.frames_content) > 0:
        EditPage(main_window.frame, frame_left, frame_right, frame_top)
    # print(frame_left.widgets_frames)


button_edit_page = ButtonTopText("Editer la page", 0, frame_top.third_top_frame, edit_page)


# Initialization of the create page button
def create_page():
    nb_buttons_max = 11
    if len(frame_left.buttons_left) < nb_buttons_max:
        NewPage(main_window.frame, frame_left, frame_right, frame_top)


button_create_page = ButtonLeftText(" + ", 20, frame_left.moving_frames[0], "white", create_page)


# Detect the window resize
def window_resize(event):
    """ Function called for each iteration of the loop """

    # If the main window is opened and resized is allowed
    if main_window.resized:
        width = main_window.frame.winfo_width()
        height = main_window.frame.winfo_height()

        # Resize the dimensions have changed
        if width != main_window.width or height != main_window.height:
            main_window.width = width
            main_window.height = height

        # Resize the window and internal elements
        frame_top.resize()
        frame_middle.resize()
        frame_left.resize()
        frame_right.resize()


# Stop the window resize
def stop_window_resize():
    """ Function called to stop the resized of the window """

    main_window.resized = False


# Bind the resize function to the main_window
main_window.frame.bind("<Configure>", window_resize)


def on_closing():
    """ Function called when the user try to close the window """

    if tk.messagebox.askokcancel("Fermer", "Voulez-vous vraiment quitter ?"):
        stop_window_resize()
        main_window.frame.destroy()


# Bind the on_closing function to the main_window protocol
main_window.frame.protocol("WM_DELETE_WINDOW", on_closing)

# Launch the GUI
main_window.frame.mainloop()





# # Widget group
# Widget_group_1 = WidgetGroup(1)
# Widget_group_2 = WidgetGroup(2)

# # Widgets
# Widget_summary = Summary(Frame_dashboard, Widget_group_1, 1)
# Widget_donut_chart = DonutChart(Frame_dashboard, Widget_group_1, 2)
# Widget_research = Filters(Frame_research, Widget_group_1, 1)
# Widget_table_1 = Table(Frame_research, Widget_group_1, 2)
# Widget_modifier = Modifiers(Frame_modification, Widget_group_1, 1)
# Widget_table_2 = Table(Frame_modification, Widget_group_2, 2)