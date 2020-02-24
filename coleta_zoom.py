import pandas as pd
import pyautogui as pag
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def coleta_zoom(search):
    search_split = '+'.join(search.split())
    driver = webdriver.Chrome('chromedriver.exe')
    zoom = driver.get('https://www.zoom.com.br/search?q={}'.format(search_split))

    xbox = pd.DataFrame()
    xbox['Modelo'] = ''
    xbox['Preco'] = ''
    xbox['Data'] = ''

    n_ofertas = len(driver.find_elements_by_xpath("//*[contains(text(), 'Ver preços')]"))
    for i in range(n_ofertas):
        ofertas = driver.find_elements_by_xpath("//*[contains(text(), 'Ver preços')]")
        ofertas[i].click()
        time.sleep(1)

        nome_produto = driver.find_element_by_class_name('product-name').text
        print(nome_produto)
        ir_historico = driver.find_element_by_xpath("//*[contains(text(), 'Ver histórico completo')]")
        ir_historico.click()
        time.sleep(4)

        produto = []
        preco = []
        data = []

        xbox_oferta = pd.DataFrame()

        x = 230
        while True:
            if x <= 678:
                pag.moveTo(x,567)
                pag.click()
                x += 7
                time.sleep(0.3)
                rect_preco = driver.find_elements_by_tag_name('svg')[5]

                if rect_preco.text != 'Criar alerta':
                    if datetime.strptime(rect_preco.text.split(' em ')[1]+'/2020','%d/%m/%Y') not in data:
                        try:
                            teste_preco = float(rect_preco.text.split(' em ')[0].replace('R$ ','').replace('.','').replace(',','.'))
                            teste_data = datetime.strptime(rect_preco.text.split(' em ')[1]+'/2020','%d/%m/%Y')
                            
                            print(rect_preco.text)
                            produto.append(nome_produto)
                            preco.append(float(rect_preco.text.split(' em ')[0].replace('R$ ','').replace('.','').replace(',','.')))
                            data.append(datetime.strptime(rect_preco.text.split(' em ')[1]+'/2020','%d/%m/%Y'))
                        except:
                            print('Deu exception')
                            continue
            else:
                break

        print()
        xbox_oferta['Modelo'] = produto
        xbox_oferta['Data'] = data
        xbox_oferta['Preço'] = preco
        
        xbox = xbox.append(xbox_oferta)

        pag.hotkey('alt','left')
        time.sleep(3)
    driver.close()
    xbox.to_excel('{}.xlsx'.format(search))

coleta_zoom('xbox one')
