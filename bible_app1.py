# bible_app.py
'''templates:

'''

# Rev 0.0.1 DEV
# Rev 0.0.2 easygui

from easygui import *
import tkinter as tk


from RL_Bible import Red_Letter_Bible



class main:
    def __init__(self):
        print('starting bible_app, loading Bible')

        self.RLbible_app = Red_Letter_Bible()

        print('Bible loaded')


    ##### Button Call Functions #####
    def RL_search(self):
        '''perform search of Red Letters
        '''
        print('RL search')

        while True:
            search_text = enterbox('enter search text', 'Advanced Search')

            if search_text == 'exit' or search_text is None:
                break

            # create scored word list
            scored_dict = self.RLbible_app.create_scored_dict(search_text)

            # search
            # uses default single verse result type
            exact_match_list, results_list = self.RLbible_app.advanced_word_search(search_text, scored_dict)

            # organize text for GUI output
            if len(exact_match_list) < 1:
                exact_match_text = 'No exact matches'
            elif len(exact_match_list) >= 20:
                exact_match_text = f'{len(exact_match_list)} exact matches\nNarrow search for results'
            else:
                exact_match_text = (f'{len(exact_match_list)} exact matches:')
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
    app = main()
    app.RL_search()

print('end script')