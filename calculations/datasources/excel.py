import calendar
import datetime
import random

import pandas as pd
from django.conf import settings

from calculations.models import BaseMeasurement

YEAR = 2023
MONTH = 4


def read_test_data(file_path: str) -> pd.DataFrame:
    data_df = pd.read_excel(file_path, index_col=[1, 0], header=[0, 1, 2])
    data_df.columns.rename(['origin', 'substance', 'type'], inplace=True)
    data_df.index.set_names(['company', 'id'], inplace=True)
    data_df.rename(columns={
        'forecast': BaseMeasurement.DataOrigin.FORECAST,
        'fact': BaseMeasurement.DataOrigin.FACT,
        'Qoil': BaseMeasurement.Substance.OIL,
        'Qliq': BaseMeasurement.Substance.LIQ,
    }, inplace=True)

    data_df = data_df.stack([0, 1, 2]).to_frame('value')

    random.seed(settings.RANDOM_SEED)  # consistency
    data_df['date'] = (
        pd.Series([
            datetime.date(YEAR, MONTH, random.randint(1, calendar.monthrange(YEAR, MONTH)[1]))
            for _ in data_df.index
        ], index=data_df.index)
        .apply(pd.Timestamp)
    )
    assert len(data_df.date.unique()) < len(data_df.index)  # has duplicate date value
    return data_df
