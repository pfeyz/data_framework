from sst.actions import *

class news():

    url = '/news'



    def news_link_url(self):
        return 'https://news.google.com/nwshp?hl=en&tab=wn'

    def sign_in_button(self):
        return get_element(text='gb_70')