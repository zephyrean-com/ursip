import itertools
import operator

import pandas as pd
from django.db import models
from django.db.models import (
    DateField,
    Sum,
)
from django.db.models.functions import Cast

from calculations.models import (
    BaseMeasurement,
    Data1,
    Data2,
)


def get_quantity_qs() -> models.QuerySet:
    def _make_qs(cls):
        return (
            cls.objects
            .annotate(_date=Cast('date', output_field=DateField()))  # sqlite type mismatch!
            .values('_date', 'substance')
            .annotate(Sum('value'))
        )
    qs1 = _make_qs(Data1)
    qs2 = _make_qs(Data2)
    return qs1.union(qs2, all=True)


def get_quantity_dict() -> dict:
    data = sorted(get_quantity_qs(), key=operator.itemgetter('_date', 'substance'))
    data_nested = {
        date: dict((k, 0) for k in BaseMeasurement.Substance.labels)
        | {
            BaseMeasurement.Substance(substance).label: sum(e['value__sum'] for e in subgroup)
            for substance, subgroup in
            itertools.groupby(group, key=operator.itemgetter('substance'))
        }
        for date, group in itertools.groupby(data, key=operator.itemgetter('_date'))
    }
    return data_nested


def get_quantity_df() -> pd.DataFrame:
    df = pd.DataFrame.from_records(get_quantity_qs())
    df.rename(columns={'_date': 'date', 'value__sum': 'sum'}, inplace=True)

    totals = df.groupby(['substance', 'date']).sum().unstack('substance', fill_value=0)
    totals.columns.set_names('metric', level=0, inplace=True)
    totals.rename(columns=dict(BaseMeasurement.Substance.choices), inplace=True)
    return totals
