from sst.actions import *

class home():

    url = '/'

    def news_link(self):
        return get_element(id='gb_5')

    def sign_in_button(self):
        return get_element(text='gb_70')