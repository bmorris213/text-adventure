# Text Adventure
# 06-02-2024
# Brian Morris

import sys
import time
import tkinter as tk
from queue import Empty
from PIL import Image, ImageTk

# Display Manager
# opens windows to display and run the game

TEXT_DELAY = 0.01

# default window themes
DEFAULT_THEMES = {
    "background" : "#ebebeb",
    "draw_color" : "#292929",
    "tile_color" : "#d4d4d4",
    "text_color" : "#1f1f1f",
    "text_bg" : "#e3e3e3",
    "font_type" : "Times New Roman",
    "normal_size" : 8 }

# Window
# default type of window object
class Window():
    def __init__(self, title_text, w_fraction, h_fraction, themes):
        # initialize theming information
        self._themes = {}
        new_themes = themes.keys()
        for name, default_theme in DEFAULT_THEMES.items():
            if name in new_themes:
                self._themes[name] = themes[name]
            else:
                self._themes[name] = default_theme
        
        # establish root top level window
        self.__root = tk.Tk()
        self.__root.title(title_text)

        # customize icon
        ico = Image.open("images/computer_icon.png")
        photo = ImageTk.PhotoImage(ico)
        self.__root.wm_iconphoto(True, photo)

        # size window to screen
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        self._base_w = int(w_fraction * screen_width)
        self._base_h = int(h_fraction * screen_height)
        x = (screen_width // 2) - (self._base_w // 2)
        y = (screen_height // 2) - (self._base_h // 2)
        self.__root.geometry(f"{self._base_w}x{self._base_h}+{x}+{y}")
        self._border_size = 5
        
        # set colors for root window
        self.__root.config(background=self._themes["tile_color"])

        # establish root behavior
        self.__is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.bind("<FocusIn>", self.wake)

        # content window frame
        self.__main_frame = tk.Frame(self.__root, highlightcolor=self._themes["draw_color"])
        self.__main_frame.config(background=self._themes["background"])
        self.__main_frame.pack(expand=True, fill=tk.BOTH,\
            padx=self._border_size, pady=self._border_size)
        
        self.content = []

    # manual wake
    def wake(self, event):
        pass
    
    # common way to add any widget to the window
    def _add_widget(self, widget_type, text_type="normal", new_f=None, **kwargs):
        if issubclass(widget_type, tk.Widget) == False:
            raise ValueError(f"Error: {widget_type} not a valid Tkinter widget")

        font_supported_widgets = [tk.Button, tk.Radiobutton,\
            tk.Entry, tk.Checkbutton, tk.Message, tk.Menubutton,\
            tk.Label, tk.Menu, tk.Text]
        
        if new_f == None:
            widget = widget_type(self.__main_frame, **kwargs)
        else:
            widget = widget_type(new_f, **kwargs)

        if type(widget) in font_supported_widgets:
            # set font sizes based on the text type
            font = self._themes["normal_size"]
            if text_type=="normal":
                font = (self._themes["font_type"], font)
            if text_type=="heading":
                font = (self._themes["font_type"], int(1.5 * font))
            elif text_type=="title":
                font = (self._themes["font_type"], int(2 * font), "bold")
            
            widget.config(font=font)

            # set colors of text object
            widget.config(background=self._themes["text_bg"])
            widget.config(highlightcolor=self._themes["draw_color"])
            widget.config(foreground=self._themes["text_color"])
        else:
            # set colors of non-text object
            widget.config(background=self._themes["tile_color"])
            widget.config(highlightcolor=self._themes["draw_color"])
        
        self.content.append(widget)
    
    def _add_group(self):
        # group is established onto a frame
        new_f = tk.Frame(self.__main_frame)
        new_f.config(background=self._themes["background"])
        new_f.config(highlightcolor=self._themes["draw_color"])
        return new_f
    
    def quit(self):
        self.__root.destroy()

    def run(self):
        self.__root.mainloop()
    
    def wait(self, miliseconds, funct):
        self.__root.after(miliseconds, funct)
    
    # action to take if window destruction call is raised
    def close(self):
        # create a confirmation popup window
        confirm = tk.Toplevel(self.__root)
        confirm.title("Confirmation")
        confirm.config(background=self._themes["background"])

        # size and center window
        width = int(self._base_w * 0.6)
        height = int(self._base_h * 0.4)
        target_width = self.__root.winfo_width()
        target_height = self.__root.winfo_height()
        x = (target_width // 2) - (width // 2) + self.__root.winfo_x()
        y = (target_height // 2) - (height // 2) + self.__root.winfo_y()
        confirm.geometry(f"{width}x{height}+{x}+{y}")

        # title the confirmation window
        label = tk.Label(confirm, text="Are you sure?\nAny unsaved progress will be lost.")
        label.config(wraplength=(width-self._border_size), justify=tk.CENTER)
        label.config(highlightcolor=self._themes["draw_color"])
        label.config(background=self._themes["text_bg"])
        label.config(foreground=self._themes["text_color"])
        label.config(font=(self._themes["font_type"], int(self._themes["normal_size"] * 1.5)))
        label.pack(fill=tk.BOTH, side=tk.TOP, expand=True,\
            padx=self._border_size, pady=self._border_size)

        # set up a frame of buttons
        button_frame = tk.Frame(confirm)
        button_frame.pack(expand=True, fill=tk.X, side=tk.BOTTOM,\
            padx=self._border_size, pady=self._border_size)

        # confirm quit
        yes_b = tk.Button(button_frame, text="Yes",\
            command=self.__root.destroy)
        yes_b.config(highlightcolor=self._themes["draw_color"])
        yes_b.config(background=self._themes["text_bg"])
        yes_b.config(foreground=self._themes["text_color"])
        yes_b.config(font=(self._themes["font_type"], self._themes["normal_size"]))
        yes_b.pack(expand=True, side=tk.LEFT, padx=self._border_size, pady=self._border_size)

        # cancel quit
        no_b = tk.Button(button_frame, text="No",\
            command=confirm.destroy)
        no_b.config(background=self._themes["text_bg"])
        no_b.config(highlightcolor=self._themes["draw_color"])
        no_b.config(foreground=self._themes["text_color"])
        no_b.config(font=(self._themes["font_type"], self._themes["normal_size"]))
        no_b.pack(expand=True, side=tk.RIGHT, padx=self._border_size, pady=self._border_size)

        # establish window
        confirm.transient(self.__root)
        confirm.grab_set()
        self.__root.wait_window(confirm)

# Game Window
# the type of window the game will be run in
class GameWindow(Window):
    # set up game themes
    game_themes = {
        "background" : "#121212",
        "draw_color" : "#434343",
        "tile_color" : "#111111",
        "text_color" : "#00db00",
        "text_bg" : "#001600",
        "flash_color" : "#004f00",
        "font_type" : "Times New Roman",
        "normal_size" : 12 }
    
    # creation of game managing window
    def __init__(self, input_handler, thread, command_queue):
        # create the basic window
        super().__init__("Text Adventure", .4, .5, self.game_themes)

        # label current location at the top
        self._add_widget(tk.Label, "title", text="Main Menu")
        self.location_title = self.content[0]
        self.location_title.pack(side=tk.TOP, fill=tk.Y, expand=True)

        # add the 'stdout' text log frame
        self.text_frame = self._add_group()
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=(self._border_size, 50))

        # bind stdout
        sys.stdout = StdoutRedirector(self.animate)

        # add the entry item
        self._add_widget(tk.Entry, "normal", self.text_frame,\
            insertbackground=self.game_themes["text_color"])
        self.entry_bar = self.content[1]
        self.entry_bar.config(disabledbackground=self.game_themes["text_bg"])
        self.entry_bar.config(disabledforeground=self.game_themes["text_color"])
        self.entry_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self._need_input = False
        self._is_animating = False

        # add the stdout textbox
        self._add_widget(tk.Text, "normal", self.text_frame,\
            wrap=tk.WORD, state=tk.DISABLED)
        self.text_log = self.content[2]
        self.text_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # add scrollbar for the textbox
        self._add_widget(tk.Scrollbar, "normal", self.text_frame,\
            command=self.text_log.yview)
        scrollbar = self.content[3]
        self.text_log.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # bind entry behavior
        self.entry_bar.bind("<Return>", self.on_enter)
        self.input_handler = input_handler
        self.entry_bar.focus_set()

        self._need_quit = False

        # wait for call to destroy
        self.gm_thread = thread
        self.wait_for_destroy()

        # wait for command to change behavior
        self.command_queue = command_queue
        self.process_commands()

    # override run
    def run(self):
        # when window syncs with thread, thread will give opening message
        self._is_animating = True
        
        # send sync request with thread
        self.input_handler.put_input("dummy input")
        # run main loop from super
        super().run()
    
    # override quit
    def quit(self, can_quit=False):
        if can_quit==True:
            super().quit()
            return

        # pause at end of page
        self.clear_screen()

        # wait for enter to kill window
        self._need_quit = True
    
    def process_commands(self):
        change_title_command = "change title:"
        try:
            command = self.command_queue.get_nowait()
            # exact matches
            if command == "clear":
                self.clear_screen()
            # starting-word matches
            elif len(command) > len(change_title_command):
                if command[:len(change_title_command)] == change_title_command:
                    self.location_title.config(text=command[len(change_title_command):])
        except Empty:
            pass
        finally:
            self.wait(100, self.process_commands)

    def wake(self, event):
        self.entry_bar.focus_set()

    # if thread closes, destroy window
    def wait_for_destroy(self):
        if self.gm_thread.is_alive() == True:
            self.wait(100, self.wait_for_destroy)
        else:
            self.quit()

    # function when user hits the enter key
    def on_enter(self, event):
        # if _need_input, we are on hold for clear screen continue
        if self._need_input == True:
            # possibly reach here through quit action
            if self._need_quit == True:
                self.quit(True)
                return
            
            self.entry_bar.config(state=tk.NORMAL)
            self.entry_bar.delete(0, tk.END)
            self._need_input = False
            self.text_log.config(state=tk.NORMAL)
            self.text_log.delete(1.0, tk.END)
            self.text_log.config(state=tk.DISABLED)
            self.input_handler.put_input("dummy input")

            # new window will create is_animating output
            self._is_animating = True
            return
        
        if self._is_animating == True:
            # are not done writing text but the user is getting impatient
            self._is_animating = False # interupt animation
            return # return window to default listening state
        
        # grab entered value
        user_input = self.entry_bar.get()
        self.entry_bar.delete(0, tk.END)

        # if entered value is nothing, return
        if user_input == "":
            return

        # print entered value for log
        self.text_log.config(state=tk.NORMAL)
        self.text_log.insert(tk.END, f" > {user_input}\n")
        self.text_log.see(tk.END)
        self.text_log.config(state=tk.DISABLED)
        self.input_handler.put_input(user_input)

        # we need to wait for terminal to finish responding before we take more input
        self._is_animating = True
    
    # clear display
    def clear_screen(self):
        # tell user we are waiting for "enter" to continue
        self.text_log.config(state=tk.NORMAL)
        self.text_log.insert(tk.END, "--- END OF PAGE ---")
        self.text_log.see(tk.END)
        self.text_log.config(state=tk.DISABLED)

        # enter a PRESS ENTER TO CONTINUE command and freeze input
        self._need_input = True
        self.entry_bar.delete(0, tk.END)
        self.entry_bar.insert(tk.END, "== Press Enter to Continue ==")
        self.entry_bar.config(state=tk.DISABLED) # wait to clear screen until input is buffered
    
    # animate text updates
    def animate(self, text):
        if self._is_animating == False:
            self.text_log.config(state=tk.NORMAL)
            self.text_log.insert(tk.END, f"{text}")
            self.text_log.see(tk.END)
            self.text_log.config(state=tk.DISABLED)
            self.color_text(self.entry_bar)
            return
        
        self.text_log.config(state=tk.NORMAL)
        self.text_log.insert(tk.END, f"{text[0]}")
        self.text_log.see(tk.END)
        self.text_log.config(state=tk.DISABLED)

        if len(text) == 1:
            # terminal is done typing
            self.color_text(self.entry_bar)
            self._is_animating = False
            return
        
        time.sleep(TEXT_DELAY)
        self.animate(text[1:])
    
    def color_text(self, text_widget):
        text_widget.config(background=self.game_themes["flash_color"])
        time.sleep(0.05)
        text_widget.config(background=self.game_themes["text_bg"])
        self._is_animating = False

# stdout print to text widget
class StdoutRedirector:
    def __init__(self, animation_function):
        self.animation_function = animation_function

    def write(self, message):
        self.animation_function(message)

    def flush(self):
        pass