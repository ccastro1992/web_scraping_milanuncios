import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

page = '/?pagina=1'


class Scraping(object):
    def __init__(self, url_base=None):
        """

        :param url_base:
        """
        self._url_base = url_base
        self._params = '?orden=relevance&fromSearch=1'

    def init_browser(self):
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install())
        return browser

    def get_content_page(self, url):
        """

        :param url:
        :return:
        """
        browser = self.init_browser()
        browser.get(url)

        cont = 1
        while True:
            scroll_height = browser.execute_script('return document.documentElement.scrollHeight')
            height = 250 * cont
            browser.execute_script('window.scrollTo(0, %s);' % (str(height)))
            if height > scroll_height:
                break
            time.sleep(1)
            cont += 1

        body = browser.execute_script('return document.body')
        source = body.get_attribute('innerHTML')

        soup = BeautifulSoup(source, 'html.parser')

        browser.close()

        return soup

    def get_subcategories(self, div_category):
        """

        :param div_category:
        :return:
        """
        sub_categories = []
        class_subcategory = 'ma-SharedCrosslinks-link ma-SharedCrosslinks-size-s ma-SharedCrosslinks-type-neutral'
        for link_subcategory in div_category.find_all('a', class_subcategory):
            sub_categories.append({
                'name': link_subcategory.attrs.get('title'),
                'url': link_subcategory.attrs.get('href')
            })
        return sub_categories

    def get_categories(self):
        """

        :return:
        """
        categories = []
        soup = self.get_content_page(self._url_base)

        for div_category in soup.find_all('div', 'sui-CollapsibleBasic is-expanded'):
            link_category = div_category.find('a', 'ma-MainCategory-mainCategoryNameLink')
            category = {
                'name': link_category.attrs.get('title'),
                'url': link_category.attrs.get('href'),
                'sub_categories': self.get_subcategories(div_category)
            }
            categories.append(category)

        return categories

    def get_advertisements(self, categories):
        """

        :param categories:
        :return:
        """

        advertisements = []

        for category in categories:
            category_url = '%s%s' % (self._url_base, category.get('url'))
            soup = self.get_content_page(category_url)

            for links_advertisement in soup.find_all('a', 'ma-AdCard-bodyTitleLink'):
                category = {
                    'name': links_advertisement.attrs.get('title'),
                    'url': links_advertisement.attrs.get('href'),
                }
                advertisements.append(category)

        return advertisements
