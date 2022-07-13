import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from recepies.models import Ingredient

root = Path(__file__).parent.parent.parent.parent.parent.parent
static_data_dir = Path(root, 'data')

FILE_LIST = {
    Path(static_data_dir, 'ingredients.csv'): Ingredient,
}


class Command(BaseCommand):
    help = 'Import ingredients from csv file'

    def handle(self, *args, **options):
        path = Path(static_data_dir, 'ingredients.csv')
        with open(path, 'r', newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            lines = list()
            head = ['name', 'measurement_unit']
            for row in reader:
                line = dict(zip(head, row))
                lines.append(line)
            creted_num = self.CreateNewObject(Ingredient, lines)
            print(f'Created {creted_num} record, object {Ingredient}')

    def CreateNewObject(self, model, lines):
        created = 0
        for line in lines:
            print(line)
            model.objects.get_or_create(**line)
            created = created + 1
        return created
