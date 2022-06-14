from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import selenium.common.exceptions as selex
from selenium.webdriver.common.by import By
import datetime
import os
import time


class PriceExctractorIport:

    def __init__(self):


        # initial settings
        headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f'user-agent={headers}')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

        # create folder for saving scraped
        if not os.path.exists(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/'):
            os.mkdir(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/')

        if not os.path.exists(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/iport/'):
            os.mkdir(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/iport/')

        if not os.path.exists(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/iport/html/'):
            os.mkdir(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/iport/html/')

    def _open_listing(self, url: str):
        # opening listing
        self.driver.get(url=url)

    def _get_file_names(self, url: str):

        self.html_path = url.split('/')[-2] + '_' + url.split('/')[-1][-1]
        self.txt_path = url.split('/')[-2]
        return self.html_path, self.txt_path

    def _save_page_source(self):

        with open(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/iport/html/{self.html_path}.html', 'w+', encoding='utf-8') as file:
            file.write(self.driver.page_source)
            file.close()

    def _get_items(self):

        self.items = self.driver.find_elements(By.CLASS_NAME, 'fresnel-container.fresnel-greaterThanOrEqual-xs')
        return self.items

    def _parse_items(self):
        self.data = []

        for item in self.items:
            item_data = {}

            item_name = item.find_element(By.CLASS_NAME, 'CatalogItemstyles__CatalogItem__Title-sc-8mov5i-5.kfzxhF').text
            item_pn = item_name.split(',')[-1].replace('/', '-').replace(')', "")
            item_href = item.find_element(By.CLASS_NAME, 'CatalogItemstyles__CatalogItem__Link-sc-8mov5i-11.eUuaeO')
            item_a = item_href.get_attribute('href')
            item_hint = item.find_element(By.CLASS_NAME, 'CatalogItemstyles__CatalogItem__DeliveryDate-sc-8mov5i-21.boDqiE').text
            item_price = item.find_element(By.CLASS_NAME, 'ProductPricestyles__ProductPrice__MainPrice-sc-1ttsy8o-2.drAJpw').text

            item_data[item_pn] = [item_a, item_name, item_price, item_hint]

            self.data.append(item_data)

        return self.data

    def _save_data_local_dict(self):

        with open(f'../../pyprojects/pricechecker/{str(datetime.date.today())}/iport/{self.txt_path}.txt', 'a', encoding='utf-8') as file:
            for item in self.data:
                file.write(f'{item}\n')
            file.close()

    def get_pagination(self):

        pagination = self.driver.find_elements(By.CLASS_NAME, 'ant-pagination-item')
        return len(pagination)

    def click_next_page_button(self):

        next_button = self.driver.find_element(By.CLASS_NAME, 'ant-btn.ant-btn-link.ant-btn-round.Buttonstyles__Button-sc-1fr199h-0.iUBptJ.Paginationstyles__PaginationArrowButton-sc-1elfdyb-1.eFiOnt')
        next_button.click()

    def run(self, url: str):

        try:
            self._open_listing(url)
            self._get_file_names(url)
            self._save_page_source()
            self._get_items()
            self._parse_items()
            self._save_data_local_dict()
            time.sleep(10)

        except Exception as ex:
            print(ex)

    def deep_run(self):

        try:
            self._get_items()
            self._parse_items()
            self._save_data_local_dict()
            time.sleep(10)

        except Exception as ex:
            print(ex)


def main(url: str):

    probe = PriceExctractorIport()
    probe.run(url)

    if probe.get_pagination() > 1:
        n = probe.get_pagination()
        i = 1

        while i <= n:
            probe.click_next_page_button()
            probe.deep_run()
            i += 1

if __name__ == '__main__':

    url = 'https://www.iport.ru/catalog/apple_iphone/'

    main(url)
