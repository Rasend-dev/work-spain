import scrapy
import pandas as pd
import re

state = str(input('ingrese el estado en donde se ejecutara la busqueda: \n'))
target = str(input('ingrese la institucion que desea investigar: \n'))

sentences = {'names': '//h1/text()',
             'address': '//div[@class="content"]//span[@itemprop="streetAddress"]/text()',
             'postal_code': '//div[@class="content"]//span[@itemprop="postalCode"]/text()',
             'phone': '//span[@class="telephone"]/b/text()',
             'email': '//div[@class="contenedor" and contains(@data-business,"customerMail")]/@data-business'}

patron_re = r'"customerMail":"([^"]+)"'

filename = f'{target}_paginas_amarillas_spain_{state}.xlsx'


class PaginasAmarillas(scrapy.Spider):
    name = 'amarillas'
    start_urls = [
        f'https://www.paginasamarillas.es/a/{target}/{state}/']
    data = {'name': [], 'address': [],
            'postal_code': [], 'phone': [], 'email': [], 'state': []}

    def parse(self, response):
        links = response.xpath(
            '//a[@href and @title and @data-omniclick="name"]/@href').getall()

        # esta sentencia xpath hace referencia al boton de siguiente pagina
        if response.xpath('//i[contains(@class,"flecha-derecha")]'):
            next_link = response.xpath(
                '//i[contains(@class,"flecha-derecha")]/../@href').get()
            # llamamos a nuestra misma funcion para poder seguir obteniendo links de las paginas
            yield response.follow(next_link, callback=self.other_parse, cb_kwargs={'links': links})
        else:
            # una vez tenemos todos los links procedemos a ejecutar la funcion in_page para investigarlos a fondo
            df = pd.DataFrame(self.data)
            df.to_excel(filename, index=False)
            for i in links:
                yield response.follow(i, callback=self.gather_page_info)

    def other_parse(self, response, **kwargs):
        links = kwargs['links']
        links.extend(response.xpath(
            '//a[@href and @title and @data-omniclick="name"]/@href').getall())

        # esta sentencia xpath hace referencia al boton de siguiente pagina
        if response.xpath('//i[contains(@class,"flecha-derecha")]'):
            next_link = response.xpath(
                '//i[contains(@class,"flecha-derecha")]/../@href').get()
            # llamamos a nuestra misma funcion para poder seguir obteniendo links de las paginas
            yield response.follow(next_link, callback=self.other_parse, cb_kwargs={'links': links})
        else:
            # una vez tenemos todos los links procedemos a ejecutar la funcion in_page para investigarlos a fondo
            df = pd.DataFrame(self.data)
            df.to_excel(filename, index=False)
            for i in links:
                yield response.follow(i, callback=self.gather_page_info)

    def gather_page_info(self, response):
        self.data['name'].append(response.xpath(
            f'{sentences["names"]}').get())
        self.data['address'].append(response.xpath(
            f'{sentences["address"]}').get())
        self.data['postal_code'].append(response.xpath(
            f'{sentences["postal_code"]}').get())
        self.data['phone'].append(response.xpath(
            f'{sentences["phone"]}').get())
        self.data['state'].append(state)
        email_text = response.xpath(sentences['email']).get()
        if email_text:
            captured_mail = re.search(patron_re, email_text).group(1)
            self.data['email'].append(captured_mail)
        else:
            self.data['email'].append('no_encontrado')

        # adding to the file section
        df = pd.read_excel(filename)
        df.append(self.data, ignore_index=True)
        df.to_excel(filename, index=False)
