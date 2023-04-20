import scrapy
import pandas as pd
import time
# page_name = str(input('ingrese la institucion que desea investigar: \n'))
# state = str(input('ingrese el estado en donde se ejecutara la busqueda: \n'))


class PaginasAmarillas(scrapy.Spider):
    name = 'amarillas'
    start_urls = [
        f'https://www.paginasamarillas.es/a/colegios-privados/guadalajara/']

    def parse(self, response):
        names = response.xpath(
            '//div[@class="box"]//h2/span[@itemprop="name"]/text()').getall()
        address = response.xpath(
            '//div[@class="box"]//span[@itemprop="streetAddress"]/text()').getall()
        postal_code = response.xpath(
            '//div[@class="box"]//span[@itemprop="postalCode"]/text()').getall()
        phone = response.xpath(
            '//div[@class="box"]//span[@itemprop="telephone"]/text()').getall()

        for i, v in enumerate(names):
            time.sleep(1)
            print(
                f'nombre: {v}\n direccion: {address[i]}\n codigo postal: {postal_code[i]}\n phone: {phone[i]}\n\n')

        # <span class="location" itemprop="address" itemscope itemtype="http://schema.org/PostalAddress"><span itemprop="streetAddress">Avenida Burgos, 3</span><span itemprop="postalCode">19005</spa
        # n><span itemprop="addressLocality">Guadalajara</span></span>
