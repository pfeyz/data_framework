import logging
from sst import runtests
logger = logging.getLogger('SST')
from sst.actions import *
from shared.pages import home_page,news_page

home = home_page.home()
news = news_page.news()

class MyAccountTests(runtests.SSTTestCase):

    set_base_url('https://www.google.com')


    def test_home_page_click_news(self):
        go_to(home.url)
        click_link(home.news_link())
        assert_url(news.news_link_url())



    def test_sign_in_click(self):
        go_to(home.url)
        click_link(home.news_link())
        news.sign_in_button().click()




