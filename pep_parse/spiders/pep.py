import scrapy

from pep_parse.items import PepParseItem

INDEX_WITH_TEXT = 0
BEGINNING_SECTION_WITH_NAME = 3
END_SECTION_WITH_NAME = -2
SECTION_WITH_NUMBER = 2


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
        pep_title = response.css('title::text').get()
        pep_number = ' '.join(pep_title.split()[:SECTION_WITH_NUMBER])
        pep_name = ' '.join(pep_title.split()[
            BEGINNING_SECTION_WITH_NAME:END_SECTION_WITH_NAME])
        data = {
            'number': pep_number,
            'name': pep_name,
            'status': response.css('abbr::text').get(),
        }
        yield PepParseItem(data)
