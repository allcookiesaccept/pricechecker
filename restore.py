from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import selenium.common.exceptions as selex
from selenium.webdriver.common.by import By
import datetime
import os
import time


class PriceExctractor:

    def __init__(self):


        # initial settings
        headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f'user-agent={headers}')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.set_window_size(1440, 900)

        # create folder for saving scraped
        if not os.path.exists(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/'):
            os.mkdir(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/')

        if not os.path.exists(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/restore/'):
            os.mkdir(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/restore/')

        if not os.path.exists(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/restore/html/'):
            os.mkdir(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/restore/html/')

    def _open_listing(self, url: str):
        # opening listing
        self.driver.get(url=url)

    def _get_file_names(self, url: str):

        self.html_path = url.split('/')[-2] + '_' + url.split('/')[-1][-1]
        self.txt_path = url.split('/')[-2]
        return self.html_path, self.txt_path

    def _save_page_source(self):

        with open(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/restore/html/{self.html_path}.html', 'w+', encoding='utf-8') as file:
            file.write(self.driver.page_source)
            file.close()

    def _get_items(self):

        self.items = self.driver.find_elements(By.CLASS_NAME, "product-card.catalog__item.product-card--buy")
        return self.items

    def _parse_items(self):

        self.data = []

        for item in self.items:
            item_data = {}

            item_href = item.find_element(By.CLASS_NAME, "product-card__link")
            item_a = item_href.get_attribute('href')
            item_pn = item_a.split('/')[-2]
            item_hint = item.find_element(By.CLASS_NAME, 'product-card__hint').text
            item_price = item.find_element(By.CLASS_NAME, "product-card__price").text
            item_name = item.find_element(By.CLASS_NAME, "product-card__name").text
            item_data[item_pn] = [item_a, item_name, item_price, item_hint]

            self.data.append(item_data)

        return self.data

    def _save_data_local_dict(self):

        with open(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/restore/{self.txt_path}.txt', 'a', encoding='utf-8') as file:
            for item in self.data:
                file.write(f'{item}\n')
            file.close()

    def get_pagination(self):

        pagination = self.driver.find_elements(By.CLASS_NAME, "pagination__item")
        return len(pagination)

    def _region_selector(self):
        element = self.driver.find_element(By.CLASS_NAME, 'choose-region.header__city')
        element.click()
        cities = self.driver.find_elements(By.CLASS_NAME, 'choose-city__city')
        cities[1].click()

    def _choose_region(self):
        element = self.driver.find_element(By.CLASS_NAME, 'btn.city-choose-mini__button.btn--gray')
        element.click()
        cities = self.driver.find_elements(By.CLASS_NAME, 'choose-city__city')
        cities[1].click()

    def run(self, url: str):

        if url.find('page=') == -1:
             try:
                self._open_listing(url)
                self._choose_region()
                self._get_file_names(url)
                self._save_page_source()
                self._get_items()
                self._parse_items()
                self._save_data_local_dict()
             except Exception as ex:
                print(ex)
        else:
            try:
                self._open_listing(url)
                self._get_file_names(url)
                self._save_page_source()
                self._get_items()
                self._parse_items()
                self._save_data_local_dict()
            except Exception as ex:
                print(ex)


def main(url: str):

    pagination_link = '?page='

    probe = PriceExctractor()
    probe.run(url)
    time.sleep(10)

    if probe.get_pagination() > 1:
        for i in range(2, probe.get_pagination()+1):
            probe.run(f'{url}{pagination_link}{i}')
            time.sleep(10)




if __name__ == '__main__':

    url = 'https://re-store.ru/apple-iphone/'

    main(url)