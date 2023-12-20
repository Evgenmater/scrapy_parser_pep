import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """Сборка ссылки на документы PEP."""
        all_peps = response.css('a.pep::attr(href)')
        for pep in all_peps:
            yield response.follow(pep, callback=self.parse_pep)

    def parse_pep(self, response):
        """Парсинг документа PEP."""
        pep_main = response.css('section#pep-content')
        pep_h1 = pep_main.css('h1::text').get()
        pep_number = ' '.join(pep_h1.split()[:2])
        pep_text = pep_main.css('h1 ::text').getall()
        join_list = ''.join(pep_text)
        pep_name = ''.join(join_list.split(pep_number))
        data = {
            'number': pep_number,
            'name': pep_name,
            'status': pep_main.css('abbr::text').get(),
        }
        yield PepParseItem(data)
