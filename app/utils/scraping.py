import time

from bs4 import BeautifulSoup
from selenium import webdriver

page = '/?pagina=1'


class Scraping(object):
    def __init__(self, url_base=None):
        self._url_base = url_base
        self._params = '?orden=relevance&fromSearch=1'

    def init_browser(self):
        """
        Metodo que inicializa un browser para acceder al sitio
        :return: browser
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        browser = webdriver.Chrome(options=chrome_options)
        return browser

    def get_content_page(self, url):
        """
        Obtiene el contenido html de la pagina solicitada
        :param url: parametro de sitio web
        :return: html del contenido del sitio web
        """
        try:
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
        finally:
            browser.quit()

        return soup

    def get_subcategories(self, div_category):
        """
        Obtiene las subcategorias del sitio web 1000anuncios.com
        :param div_category: div de la categoria donde vamos a buscar las subcategorias (child)
        :return: html de la subcategoria
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
        Obtiene las categorias del sitio web 1000anuncios.com
        :return: html de la categoria
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
        Obtiene los anuncios del sitio web 1000anuncios.com
        :param categories: parametro de filtro de los anuncios
        :return: html de los anuncios correspondientes a categoria
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
