import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import os
from deep_translator import GoogleTranslator
import utilidades

site = 'https://www.bonopet.com.br/collections/todos-produtos'
requisicao = requests.get(site)
conteudo = requisicao.content
conteudo_scraped = bs(conteudo, 'html.parser')
navegacao = conteudo_scraped.find('div', attrs={'class':'pagination__nav'})

def traduz_descricao_produtos():
    for pagina in range(len(navegacao)):
        requisicao_atual = requests.get(f'https://www.bonopet.com.br/collections/todos-produtos?page={pagina + 1}')
        sleep(1)
        sopa_atual = bs(requisicao_atual.content)
        sleep(1)
        produtos_da_pagina_atual = sopa_atual.find_all('a', attrs={'class': 'product-item__title text--strong link'})
        for produto in produtos_da_pagina_atual:
            nome_produto = utilidades.ajusta_nome(produto.text)
            link_produto = f'https://www.bonopet.com.br/{produto["href"]}'
            diretorio_produto = os.path.join('Produtos', nome_produto)
            
            if not os.path.exists(diretorio_produto):
                os.mkdir(diretorio_produto)
                with open(f'{diretorio_produto}\\original.txt', 'w') as arquivo:
                    conteudo = utilidades.obtem_descricao_produto(link_produto)
                    arquivo.write(conteudo)
                
                with open(f'{diretorio_produto}\\traduzido.txt', 'w') as arquivo:
                    conteudo_original = utilidades.obtem_descricao_produto(link_produto)
                    conteudo_traduzido = GoogleTranslator(source='pt', target='en').translate(conteudo_original)
                    arquivo.write(conteudo_traduzido)

if __name__ == '__main__':
    traduz_descricao_produtos()
