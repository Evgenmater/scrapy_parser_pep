from pathlib import Path

from datetime import datetime

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:

    def open_spider(self, spider):
        self.quantity_status = {'Total': 0}
        results = BASE_DIR / 'results'
        file = f'status_summary_{datetime.now():%Y-%m-%d-%H-%M}.csv'
        results.mkdir(exist_ok=True)
        self.filename = results / file

    def process_item(self, item, spider):

        if item['status'] in self.quantity_status:
            self.quantity_status[item['status']] += 1
        else:
            self.quantity_status[item['status']] = 1
        self.quantity_status['Total'] += 1

        return item

    def close_spider(self, spider):

        with open(self.filename, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for key, value in self.quantity_status.items():
                f.write(f'{key},{value}\n')
