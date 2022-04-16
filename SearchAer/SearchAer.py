from selenium.webdriver.common.by import By
from abc import ABC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import os


class Site(webdriver.Chrome):
    def __init__(self, fecha_navegador=False):
        self.fecha_navegador = fecha_navegador
        self .pn = (By.NAME, 's')
        self.submit = (By.XPATH, '//*[@id="aws_widget-2"]/div[2]/form/div[2]')
        super(Site, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fecha_navegador:
            self.quit()

    def open_page(self):
        self.get('https://www.barataaviation.com.br/')

    def busca_pn(self):
        self.find_element_by_name('s').send_keys('teste')
        self.find_element_by_xpath('//*[@id="aws_widget-2"]/div[2]/form/div[2]').click()

with Site() as bot:
    bot.open_page()
    pn = 'teste'
    bot.busca_pn(pn)

