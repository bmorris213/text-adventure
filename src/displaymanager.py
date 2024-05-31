# Text Adventure
# 05-30-24
# Brian Morris

import tkinter as tk

# Display Manager
# manages the window in which game will run

# ButtonGroup
# Encapsulates a group of selectable buttons
class ButtonGroup():
    def __init__(self, parent, is_vertical=True):
        self.__parent = parent
        self.__items = []
        self.__commands = {}
        self.current_index = 0
        self.is_vertical = is_vertical

        # draw selector
        self.selector = tk.Canvas(self.__parent, width=20, height=200)
        self.selector.create_polygon(10, 10, 20, 15, 10, 20, fill="blue")

    def move_selector(self, index):
        selection = self.get_item()
        w_x = selection.winfo_x()
        w_y = selection.winfo_y()
        w_height = selection.winfo_height()

        if isinstance(self.__items[index], ButtonGroup):
            self.__items[index].selector.place(x=w_x - 20, y=w_y + w_height//2 - 10)
        else:
            self.selector.place(x=w_x - 20, y=w_y + w_height//2 - 10)
    
    def change_selection(self, direction, vertical=False):
        if len(self.__items) != 0:
            selection = self.__items[self.current_index]
            
            if vertical == True:
                # check if previous item was a group
                if isinstance(self.__items[self.current_index], ButtonGroup):
                    self.selector.itemconfig(1, state='normal')
                    self.__items[self.current_index].selector.itemconfig(1, state='hidden')

                self.current_index = (self.current_index - direction) % len(self.__items)
                self.move_selector(self.current_index)

                # check if new item is a group
                if isinstance(self.__items[self.current_index], ButtonGroup):
                    self.__items[self.current_index].selector.itemconfig(1, state='normal')
                    self.selector.itemconfig(1, state='hidden')
                
            elif isinstance(selection, ButtonGroup) == True:
                selection.current_index = (selection.current_index + direction) % selection.count()
                self.move_selector(self.current_index)
            
    
    def add_button(self, text, command, is_vertical=True):
        btn = tk.Button(self.__parent, text=text, command=command, anchor="w")
        if is_vertical == True:
            btn.pack()
        else:
            btn.pack(side = tk.LEFT, padx=30)
        self.__commands[text] = command
        self.__items.append(btn)
    
    def count(self):
        return len(self.__items)
    
    def add_group(self, command_dict):
        if self.is_vertical == True:
            newf = tk.Frame(self.__parent)
            horizontal_group = ButtonGroup(newf, False)
            for text, command in command_dict.items():
                horizontal_group.add_button(text, command, False)
            newf.pack()
            self.__items.append(horizontal_group)

    def get_item(self):
        selection = self.__items[self.current_index]
        if isinstance(selection, ButtonGroup) == True:
            selection = selection.get_item()
        return selection
    
    def activate_selection(self):
        print(self.get_item)

# Window
# Encapsulates graphical display for the program
class Window():
    def __init__(self, width, height):
        self.__root = tk.Tk()
        self.__root.title("Text Adventure")
        self.__root.geometry(f"{width}x{height}")
        self.__is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__selections = ButtonGroup(self.__root)
        self.__root.bind("<KeyPress>", self.handle_key_press)
    
    # handle keyboard input
    def handle_key_press(self, event):
        if event.keysym == 'Up':
            self.__selections.change_selection(1, True)
        elif event.keysym == 'Down':
            self.__selections.change_selection(-1, True)
        if event.keysym == 'Right':
            self.__selections.change_selection(1, False)
        elif event.keysym == 'Left':
            self.__selections.change_selection(-1, False)
        elif event.keysym == 'Return':
            self.__selections.activate_selection()
    
    # handle frame updates
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    # run until close
    def wait_for_close(self):
        self.__is_running = True
        self.redraw()
        self.__selections.move_selector(self.__selections.current_index)
        self.redraw()

        while (self.__is_running == True):
            self.redraw()
    
    # end program protocol
    def close(self):
        self.__is_running = False
    
    # add a label object to the canvas
    def add_title(self, text):
        text_var = tk.StringVar()
        text_var.set(text)
        label = tk.Label(self.__root, textvariable=text_var)
        label.pack()
    
    # add selection
    def add_selection(self, command_dict):
        self.__selections.add_group(command_dict)
    
    # add button
    def add_button(self, text, command):
        self.__selections.add_button(text, command)

# Main Menu
# encapsulates the main menu window
class MainMenu(Window):
    def __init__(self):
        super().__init__(800, 500)

        self.add_title("Main Menu")

        self.add_button("Load Game", _load_game)
        self.add_button("Continue", _continue_game)
        self.add_button("New Game", _new_game)
        self.add_button("Quit", _quit_game)

        horizontal_selection = { "Option 1" : _option_1,
            "Option 2" : _option_2,
            "Option 3" : _option_3 }
        
        self.add_selection(horizontal_selection)

def _option_1():
    pass
def _option_2():
    pass
def _option_3():
    pass
def _load_game():
    pass
def _continue_game():
    pass
def _new_game():
    pass
def _quit_game():
    pass