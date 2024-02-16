import requests
from bs4 import BeautifulSoup as bs

def ajusta_nome(texto):
    nome_produto = texto.split('|')[0].rstrip()
    if u"\u2122" or u"\u00AE" in nome_produto:
        nome_produto_ajustado = nome_produto.replace("™", "").replace("®", "")
    return nome_produto_ajustado

def obtem_descricao_produto(link_produto):
    requisicao = requests.get(link_produto)
    conteudo = requisicao.content
    descricao = bs(conteudo, 'html.parser').find('div', attrs={'class':'product-block-list__item product-block-list__item--description'}).text
    return descricao