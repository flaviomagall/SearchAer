# -*- coding: utf-8 -*-

from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import shutil
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


SITES_PESQUISA = {'Fibraer': 'https://loja.fibraer.com.br/',
                  'GlobalParts': 'https://www.globalp.com.br/produtos/',
                  'BarataAviation': 'https://www.barataaviation.com.br/',
                  'SommaAviation': 'https://loja.sommaaviation.com.br/'}

"""_summary_

    ANALISAR->

    # trata_nomes não funciona, aparentemente retorna a mesma coisa da entrada
    # analisar melhor o segura para implementar o EC corretamente
    # Mudar a ordem de chamada do navegador com o o for do pn
    """


def df_dados():
    """Seleciona um arquivo excel com lista de PNs com o cabeçalho "PN"."""
    # Abre janela para localizar arquivo de leitura
    Tk().withdraw()
    addr = askopenfilename()
    return pd.read_excel(addr, converters={'PN': str}).drop_duplicates()


class OrganizaArquivos:
    """
    Realiza todas as necessidades de criar, gerenciar e tratar arquivos.
    """

    def cria_pasta(self, li_pn):
        """
        Analisa se já existe a pasta nomeada com o PN, caso não encontre, cria uma pasta nova para o PN.
        Args:
            li_pn (DataFrame): retirado do df_dados contendo a relação de itens para busca.
        """
        destino_pastas = os.path.join(os.getcwd(), 'arquivos_saida')
        if 'arquivos_saida' not in os.listdir():
            os.mkdir('arquivos_saida')
        specialchars = '\/:*?"<>|,'
        for PN in li_pn['PN']:
            for specialchar in specialchars:
                PN = PN.replace(specialchar, ' ')
            if pn not in os.listdir(destino_pastas):
                os.mkdir(os.path.join(destino_pastas, pn))

    def move_img(self, file_name, pn):
        """
        Pega as screenshots e move para a pasta do referido item.
        Args:
            file_name (Str): Variável definida para receber o futuro nome da screenshot depois de tratada pela func: trata_nomes.
            pn (St): Nome de cada item da lista criada pelo df_dados: li_pn.
        """
        destino_pastas = os.path.join(os.getcwd(), 'arquivos_saida')
        self.file_name = file_name
        origem_img = os.path.join(os.getcwd(), file_name)
        destino_img = os.path.join(destino_pastas, pn)
        try:
            shutil.move(origem_img, destino_img)
        except:
            pass

    def trata_nomes(self, pn, site):
        """
        Garante que nenhuma pasta e img.png tenha caracteres que impossibilitem a nomeação do mesmo.
        Pode ser substituida futuramente por Regex no próprio elemento.
        Args:
            pn (St): Nome de cada item da lista criada pelo df_dados: li_pn.
        Returns:
            Str: nome aceito para crição de pasta e no padrão ideal para futura pesquisa.
        """
        self.pn = pn
        specialChars = '\/:*?"<>|,'
        for specialChar in specialChars:
            pn = pn.replace(specialChar, ' ')
        return f'{pn} - {site}.png'


class Navegador:
    """
    Define um navegador para todas as buscas nos sites.
    """
    navegador = webdriver.Chrome(ChromeDriverManager().install())
    segura_site = ui.WebDriverWait(navegador, 30)
    segura_pn = ui.WebDriverWait(navegador, 1)

    def __init__(self, site):
        self.site = site
        OrganizaArquivos().cria_pasta(li_pn)
        self.seleciona_sites()

    def seleciona_sites(self):
        if self.site == 'Fibraer':
            Fibraer(self.site)
        elif self.site == 'GlobalParts':
            GlobalParts(self.site)
        elif self.site == 'BarataAviation':
            BarataAviation(self.site)
        else:
            SommaAviation(self.site)


class Fibraer(Navegador):
    insert_pn = (By.ID, 'auto-complete')
    submit_pn = (By.XPATH, '//*[@id="form-buscar"]/button')
    back_without_find = (By.CSS_SELECTOR,
                         'a[title="Voltar para página inicial"]')
    pn_found = (By.CLASS_NAME, 'imagem-principal')

    def __init__(self, site):
        self.site = site
        self.abre_navegador()
        self.busca_pn(pn)

    def abre_navegador(self):
        self.navegador.get(SITES_PESQUISA[self.site])
        print(f'Pesquisando {pn}...')
        try:
            self.segura_site.until(
                lambda driver: driver.find_element(*self.submit_pn))
        except TimeoutException:
            print("Loading took too much time!")

    def busca_pn(self, pn):
        self.navegador.find_element(*self.insert_pn).send_keys(pn)
        self.navegador.find_element(*self.submit_pn).click()
        try:
            self.segura_pn.until(
                lambda driver: driver.find_element(*self.back_without_find))
            file_name = OrganizaArquivos().trata_nomes(pn, site)
            pyautogui.screenshot(
                imageFilename=file_name, region=(1280, 0, 1280, 1440))
            sleep(1)
            OrganizaArquivos().move_img(file_name, pn)
        except TimeoutException:
            try:
                self.segura_pn.until(
                    lambda driver: driver.find_element(*self.pn_found))
                file_name = OrganizaArquivos().trata_nomes(pn, site)
                print(file_name)
                pyautogui.screenshot(
                    imageFilename=file_name, region=(1280, 0, 1280, 1440))
                sleep(1)
                OrganizaArquivos().move_img(file_name, pn)
                print('Encontrei')
            except TimeoutException:
                print("Loading took too much time!")
                pass


class GlobalParts(Navegador):
    insert_pn = (By.ID, 'yith-s')
    submit_pn = (By.ID, 'yith-searchsubmit')
    back_without_find = (By.ID, 'content')
    pn_found = (By.CLASS_NAME,
                'woocommerce-LoopProduct-link woocommerce-loop-product__link')

    def __init__(self, site):
        self.site = site
        self.abre_navegador()
        self.busca_pn(pn)

    def abre_navegador(self):
        self.navegador.get(SITES_PESQUISA[self.site])
        print(f'Pesquisando {pn}...')
        try:
            self.segura_site.until(
                lambda driver: driver.find_element(*self.submit_pn))
        except TimeoutException:
            print("Loading took too much time!")

    def busca_pn(self, pn):
        self.navegador.find_element(*self.insert_pn).send_keys(pn)
        self.navegador.find_element(*self.submit_pn).click()
        try:
            self.segura_pn.until(
                lambda driver: driver.find_element(*self.back_without_find))
            file_name = OrganizaArquivos().trata_nomes(pn, site)
            pyautogui.screenshot(
                imageFilename=file_name, region=(1280, 0, 1280, 1440))
            sleep(1)
            OrganizaArquivos().move_img(file_name, pn)
            self.navegador.find_element(*self.insert_pn).clear()
        except TimeoutException:
            try:
                self.segura_pn.until(
                    lambda driver: driver.find_element(*self.pn_found))
                file_name = OrganizaArquivos().trata_nomes(pn, site)
                pyautogui.screenshot(
                    imageFilename=file_name, region=(1280, 0, 1280, 1440))
                sleep(1)
                OrganizaArquivos().move_img(file_name, pn)
                self.navegador.find_element(*self.insert_pn).clear()
                print('Encontrei')
            except TimeoutException:
                print("Loading took too much time!")
                pass


class BarataAviation(Navegador):
    insert_pn = (By.NAME, 's')
    submit_pn = (By.CLASS_NAME, 'aws-search-btn aws-form-btn')
    back_without_find = (By.CSS_SELECTOR, 'p[class="woocommerce-info"]')
    pn_found = (By.CLASS_NAME,
                'woocommerce-ordering')

    def __init__(self, site):
        self.site = site
        self.abre_navegador()
        self.busca_pn(pn)

    def abre_navegador(self):
        self.navegador.get(SITES_PESQUISA[self.site])
        print(f'Pesquisando {pn}...')
        try:
            self.segura_site.until(
                lambda driver: driver.find_element(*self.submit_pn))
        except TimeoutException:
            print("Loading took too much time!")

    def busca_pn(self, pn):
        self.navegador.find_element(*self.insert_pn).send_keys(pn)
        self.navegador.find_element(*self.submit_pn).click()
        try:
            self.segura_pn.until(
                EC.presence_of_element_located(*self.back_without_find))
            file_name = OrganizaArquivos().trata_nomes(pn, site)
            pyautogui.screenshot(
                imageFilename=file_name, region=(1280, 0, 1280, 1440))
            sleep(1)
            OrganizaArquivos().move_img(file_name, pn)
            self.navegador.execute_script("window.history.go(-1)")
            self.segura_site.until(
                lambda driver: driver.find_element(*self.submit_pn))
        except TimeoutException:
            try:
                self.segura_pn.until(
                    EC.presence_of_element_located(*self.pn_found))
                file_name = OrganizaArquivos().trata_nomes(pn, site)
                pyautogui.screenshot(
                    imageFilename=file_name, region=(1280, 0, 1280, 1440))
                sleep(1)
                OrganizaArquivos().move_img(file_name, pn)
                self.navegador.execute_script("window.history.go(-1)")
                self.segura_site.until(
                    lambda driver: driver.find_element(*self.submit_pn))
                print('Encontrei')
            except TimeoutException:
                print("Loading took too much time!")
                pass


class SommaAviation(Navegador):
    insert_pn = (By.ID, 'auto-complete')
    submit_pn = (By.CSS_SELECTOR, 'button[style="color: rgb(0, 0, 0);"]')
    back_without_find = (
        By.CSS_SELECTOR, 'a[title="Voltar para página inicial"]')
    pn_found = (By.ID, 'listagemProdutos')

    def __init__(self, site):
        self.site = site
        self.abre_navegador()
        self.busca_pn(pn)

    def abre_navegador(self):
        self.navegador.get(SITES_PESQUISA[self.site])
        print(f'Pesquisando {pn}...')
        try:
            self.segura_site.until(
                lambda driver: driver.find_element(*self.submit_pn))
        except TimeoutException:
            print("Loading took too much time!")

    def busca_pn(self, pn):
        self.navegador.find_element(*self.insert_pn).send_keys(pn)
        self.navegador.find_element(*self.submit_pn).click()
        try:
            self.segura_pn.until(
                EC.presence_of_element_located(*self.back_without_find))
            file_name = OrganizaArquivos().trata_nomes(pn, site)
            pyautogui.screenshot(
                imageFilename=file_name, region=(1280, 0, 1280, 1440))
            sleep(1)
            OrganizaArquivos().move_img(file_name, pn)
            self.navegador.find_element(*self.insert_pn).clear()
        except TimeoutException:
            try:
                self.segura_pn.until(
                    EC.presence_of_element_located(*self.pn_found))
                file_name = OrganizaArquivos().trata_nomes(pn, site)
                pyautogui.screenshot(
                    imageFilename=file_name, region=(1280, 0, 1280, 1440))
                sleep(1)
                OrganizaArquivos().move_img(file_name, pn)
                self.navegador.find_element(*self.insert_pn).clear()
                print('Encontrei')
            except TimeoutException:
                print("Loading took too much time!")
                pass


li_pn = df_dados()
for site in SITES_PESQUISA:
    for pn in li_pn['PN']:
        Navegador(site)
