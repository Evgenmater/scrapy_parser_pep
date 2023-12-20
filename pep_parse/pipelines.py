import csv
from pathlib import Path

from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATETIME_FORMAT = '%Y-%m-%d-%H-%M-%S'


class PepParsePipeline:

    def open_spider(self, spider):
        self.quantity_status = {}
        results = BASE_DIR / 'results'
        file = f'status_summary_{datetime.now().strftime(DATETIME_FORMAT)}.csv'
        results.mkdir(exist_ok=True)
        self.filename = results / file

    def process_item(self, item, spider):

        if item['status'] in self.quantity_status:
            self.quantity_status[item['status']] += 1
        else:
            self.quantity_status[item['status']] = 1

        return item

    def close_spider(self, spider):

        with open(self.filename, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])
            total = 0
            for key, value in self.quantity_status.items():
                total += value
                writer.writerow([key, value])
            writer.writerow(['Total', total])
