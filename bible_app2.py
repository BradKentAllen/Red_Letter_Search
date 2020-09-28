'''templates:
1.  clean and kill buttons for GUI with cards
'''

# Rev 1: reformatted

import tkinter as tk
import tkinter.ttk as ttk
from easygui import *

from RL_Bible import Red_Letter_Bible

# global killNow is used to stop all functions (kill) vs clean
global killNow

class main(tk.Tk):
    def __init__(self):
        self.next_card = 0

        self.RLbible_app = Red_Letter_Bible()

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