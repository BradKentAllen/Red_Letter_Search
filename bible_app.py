# bible_app.py

# Rev 0.0.1 DEV
# Rev 0.0.2 easygui
# Rev 0.0.3 add startup message


import tkinter as tk
import tkinter.ttk as ttk
from easygui import *
import time
import threading

from RL_Bible import Red_Letter_Bible

# global killNow is used to stop all functions (kill) vs clean
global killNow

class main(tk.Tk):
    def __init__(self):
        self.load_Bible()
    
        tk.Tk.__init__(self)
        self.title('Red Letter Search')
        self.geometry('%dx%d+%d+%d' % (400, 300, 500, 100))
        
        # Set up frames
        self.wrapperMain = tk.Frame(self)
        self.wrapperMain.pack()
        headerMain = tk.Frame(self.wrapperMain, padx=20, pady=20)
        header_text = 'Enter phrase to search'
        header_label = tk.Label(headerMain, text=header_text)
        header_label.pack()
        headerMain.pack()
        frameControl = tk.Frame(self.wrapperMain, padx=10, pady=10)
        frameControl.columnconfigure(0, weight=1)
        frameControl.pack()
        #self.frameDisplay = tk.Frame(self.wrapperMain, padx=10, pady=30)
        #self.frameDisplay.columnconfigure(0, weight=1)
        #self.frameDisplay.pack()
        frameBottom = tk.Frame(self.wrapperMain, padx=10, pady=10)
        frameBottom.columnconfigure(0, weight=1)
        frameBottom.pack()

        # inputs
        self.text_input = tk.Entry(frameControl, width=100)
        self.text_input.focus_set()
        self.text_input.pack()
        frame_search = tk.Frame(frameControl, relief=tk.RAISED, borderwidth=5)
        frame_search.pack(side=tk.TOP, pady=5, padx=30)
        button_search = tk.Button(frame_search, text="Search", command=self.RL_search)
        button_search.config(width=300)
        button_search.pack()


        # clean and kill buttons
        cleanButton = ttk.Button(self, text="Clean", command=self.clean_cards)
        cleanButton.pack(side=tk.LEFT, padx=60)

        killButton = ttk.Button(self, text="Exit", command=self.killSession)
        killButton.pack(side=tk.LEFT, padx=60)

        self.mainloop()

    def load_Bible(self):
        '''Show start up message while loading
        '''
        # define root window but will be withdrawn
        root = tk.Tk()

        # this is the window that shows
        window = tk.Toplevel() # or tkinter.Tk()

        # withdraw root window
        root.withdraw()

        window.title('Loading')
        window.geometry('%dx%d+%d+%d' % (400, 300, 500, 100))
        label = tk.Label(window, text = "Loading RL Bible\n\nPlease Wait")
        label.pack(side=tk.TOP, anchor=tk.W)

        # start thread and run startup in separate call function
        thread = threading.Thread(target = self.startup_call)
        thread.start() # start parallel computation
        while thread.is_alive():
            # code while computing
            window.update()
            time.sleep(0.001)

        # code when computation is done
        root.destroy()

    def startup_call(self):
        '''Defines loads during startup
        '''
        self.RLbible_app = Red_Letter_Bible()
        #self.done.append(self.RLbible_app)

    def clean_cards(self):
        '''cleans all popup cards and resets next_card
        '''
        self.destroy()
        self.next_card = 0

    def killSession(self):
        """Changes global killNow to shut down.
        """
        global killNow
        killNow = False
        self.destroy()

    ##### Button Call Functions #####
    def RL_search(self):
        '''perform search of Red Letters
        Present results in easyGUI text box
        '''
        print('RL search')

        search_text = self.text_input.get()

        if search_text == 'exit' or search_text is None:
            self.clean_cards()

        # create scored word list
        scored_dict = self.RLbible_app.create_scored_dict(search_text)

        # search
        # uses default single verse result type
        exact_match_list, results_list = self.RLbible_app.advanced_word_search(search_text, scored_dict)

        # organize text for GUI output
        if len(exact_match_list) < 1:
            exact_match_text = f'No exact matches for\n{search_text}'
        elif len(exact_match_list) >= 20:
            exact_match_text = f'{len(exact_match_list)} exact matches for\n{search_text}\nNarrow search for results'
        else:
            exact_match_text = (f'{len(exact_match_list)} exact matches for\n{search_text}')
            for result in exact_match_list:
                exact_match_text = (f'{exact_match_text}\n\n{result[2]} ({result[0]} {result[1]})')

        if len(results_list) == 0:
            results_text = 'no results'
        else:
            results_text = (f'{len(results_list)} results found:')
            for result in results_list:
                results_text = f'{results_text}\n\n(score: {result[3]}) {result[2]} ({result[0]} {result[1]})'

        textbox(msg=exact_match_text, title='Results', text=results_text)



### MAIN EXECUTION ###
if __name__ == '__main__':
    global killNow

    killNow = True
    while killNow:
        main()

print('end script')