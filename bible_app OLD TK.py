'''templates:
1.  clean and kill buttons for GUI with cards
'''

# Rev 1: reformatted

import tkinter as tk
import tkinter.ttk as ttk

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
        headerMain.pack()
        frameControl = tk.Frame(self.wrapperMain, padx=0, pady=10)
        frameControl.columnconfigure(0, weight=1)
        frameControl.pack()
        self.frameDisplay = tk.Frame(self.wrapperMain, padx=10, pady=30)
        self.frameDisplay.columnconfigure(0, weight=1)
        self.frameDisplay.pack()
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

        killButton = ttk.Button(self, text="Done", command=self.killSession)
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
        '''
        print('RL search')

        search_text = self.text_input.get()

        # create scored word list
        scored_dict = self.RLbible_app.create_scored_dict(search_text)

        # search
        # uses default single verse result type
        exact_match_list, results_list = self.RLbible_app.advanced_word_search(search_text, scored_dict)

        # organize text for GUI output
        if len(exact_match_list) == 0:
            exact_match_text = 'No exact matches'
        elif len(exact_match_list) >= 20:
            exact_match_text = (f'{len(exact_match_list)} exact matches\nNarrow search for results')
        else:
            exact_match_text = (f'{len(exact_match_list)} exact matches:')
            for result in exact_match_list:
                exact_match_text = (f'{exact_match_text}\n\n{result[2]} ({result[0]} {result[1]})')


        #### create window
        child = tk.Toplevel()
        child.title(search_text[:20])

        # place card
        card_X = 10 + (50 * self.next_card)
        card_Y = 10 + (50 * self.next_card)
        child.geometry("500x800+%d+%d" % (card_X, card_Y))

        # example2 code
        # create canvas widget
        scroll_canvas = tk.Canvas(child, width=500, height = 400, scrollregion=(0,0,480,800))

        # scrollbar associated with canvas widget
        scroll_bar = ttk.Scrollbar(scroll_canvas, orient="vertical")
        scroll_bar.pack(side="right", expand=True, fill="y")
        
        scroll_bar.config(command=scroll_canvas.yview)
        scroll_canvas.config(yscrollcommand = scroll_bar.set)

        scroll_canvas.pack(side='left', fill='both')

        text_frame = tk.Frame(scroll_canvas)
        text_frame.pack()

        text_label = tk.Label(text_frame, wraplength=450, text=exact_match_text)
        text_label.pack(side="left", fill="both", expand=True)

        
        #text_box.configure(yscrollcommand=scroll_y.set)
        #text_box['yscrollcommand'] = scroll_y.set

        #wrapper = tk.Frame(child, padx=5, pady=10)
        #wrapper.pack(side=tk.LEFT, anchor=tk.N)
        


        # end example2

        ''' example code
        card_canvas = tk.Canvas(child, borderwidth=0)
        card_frame = tk.Frame(card_canvas)
        card_vsb = tk.Scrollbar(child, orient="vertical", command=card_canvas.yview)
        card_canvas.configure(yscrollcommand=card_vsb.set)

        card_vsb.pack(side="right", fill="y")
        card_canvas.pack(side="left", fill="both", expand=True)

        card_frame.configure(yscrollcommand=card_vsb.set)
        #card_canvas.create_window((4,4), window=self.frame, anchor="nw",tags="self.frame")

        # end example
        '''

        ''' WORKS:
        wrapper = tk.Frame(child, padx=5, pady=10)
        wrapper.pack(side=tk.LEFT, anchor=tk.N)
        text_box = tk.Text(wrapper,)
        text_box_label = tk.Label(wrapper, wraplength=450, text=exact_match_text)
        text_box_label.pack(side="left", fill="both", expand=True)
        '''

        self.next_card += 1


### MAIN EXECUTION ###
if __name__ == '__main__':
    global killNow

    killNow = True
    while killNow:
        main()

print('end script')