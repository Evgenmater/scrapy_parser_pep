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
        pep_h1 = pep_main.css('h1::text').get().replace(' – ', '///', 1)
        pep_number_and_name = pep_h1.split('///')
        data = {
            'number': pep_number_and_name[0],
            'name': pep_number_and_name[1],
            'status': pep_main.css('abbr::text').get(),
        }
        yield PepParseItem(data)
