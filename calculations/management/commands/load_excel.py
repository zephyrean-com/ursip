import pandas as pd
from django.core.management import BaseCommand

from calculations import (
    actions,
    datasources,
)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        data_df: pd.DataFrame = datasources.excel.read_test_data(options['file_path'])
        actions.bulk_upload_data(data_df)
