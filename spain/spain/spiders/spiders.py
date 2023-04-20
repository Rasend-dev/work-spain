import scrapy
import pandas as pd
import time

state = str(input('ingrese el estado en donde se ejecutara la busqueda: \n'))
target = str(input('ingrese la institucion que desea investigar: \n'))

sentences = {'names': '//div[@class="box"]//h2/span[@itemprop="name"]/text()',
             'address': '//div[@class="box"]//span[@itemprop="streetAddress"]/text()',
             'postal_code': '//div[@class="box"]//span[@itemprop="postalCode"]/text()',
             'phone': '//div[@class="box"]//span[@itemprop="telephone"]/text()'}


class PaginasAmarillas(scrapy.Spider):
    name = 'amarillas'
    start_urls = [
        f'https://www.paginasamarillas.es/a/{target}/{state}/']
    data = {'name': [], 'address': [],
            'postal_code': [], 'phone': [], 'state': []}

    def parse(self, response):
        names = response.xpath(
            f'{sentences["names"]}').getall()
        address = response.xpath(
            f'{sentences["address"]}').getall()
        postal_code = response.xpath(
            f'{sentences["postal_code"]}').getall()
        phone = response.xpath(
            f'{sentences["phone"]}').getall()

        # esta sentencia xpath hace referencia al boton de siguiente pagina
        if response.xpath('//i[contains(@class,"flecha-derecha")]'):
            next_link = response.xpath(
                '//i[contains(@class,"flecha-derecha")]/../@href').get()
            self.data['name'].extend(names)
            self.data['address'].extend(address)
            self.data['postal_code'].extend(postal_code)
            self.data['phone'].extend(phone)
            yield response.follow(f'{next_link}', callback=self.next_page)
        else:
            self.data['state'].extend([state for i in self.data['name']])
            df = pd.DataFrame(self.data)
            df.to_excel(f'{target}_paginas_amarillas_spain.xlsx', index=False)

    def next_page(self, response):
        self.data['name'].extend(response.xpath(
            f'{sentences["names"]}').getall())
        self.data['address'].extend(response.xpath(
            f'{sentences["address"]}').getall())
        self.data['postal_code'].extend(response.xpath(
            f'{sentences["postal_code"]}').getall())
        self.data['phone'].extend(response.xpath(
            f'{sentences["phone"]}').getall())

        if response.xpath('//i[contains(@class,"flecha-derecha")]'):
            next_link = response.xpath(
                '//i[contains(@class,"flecha-derecha")]/../@href').get()
            yield response.follow(f'{next_link}', callback=self.next_page)
        else:
            self.data['state'].extend([state for i in self.data['name']])
            df = pd.DataFrame(self.data)
            df.to_excel(f'{target}_paginas_amarillas_spain.xlsx', index=False)
