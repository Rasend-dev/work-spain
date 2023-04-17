import scrapy
import pandas as pd

page_name = str(input('ingrese la institucion que desea investigar'))
state = str(input('ingrese el estado en donde se ejecutara la busqueda'))


class PaginasAmarillas(scrapy.Spider):
    name = 'amarillas'
    start_urls = [
        f'https://www.paginasamarillas.es/a/{page_name}/{state}/']

    def parse(self, response):
        pass
