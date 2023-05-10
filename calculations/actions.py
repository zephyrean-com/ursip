import functools
import operator

import pandas as pd
import sqlalchemy

from calculations.datasources import sqlite
from calculations.models import (
    Company,
    Data1,
    Data2,
)


def bulk_upload_data(data_df: pd.DataFrame):
    data_df = data_df.copy()
    company_names = data_df.index.unique('company')
    Company.objects.bulk_create(
        [
            Company(name=name)
            for name in company_names
        ],
        ignore_conflicts=True,
    )
    company_index = {
        name: pk
        for pk, name in
        (
            Company.objects
            .filter(name__in=company_names)
            .values_list('pk', 'name')
        )
    }
    data_df.reset_index(level=['company', 'id', 'origin', 'substance'], inplace=True)

    data_df['company_id'] = data_df.company.apply(
        functools.partial(
            operator.getitem,
            company_index,
        )
    )
    # # alternatively:
    # data_df['company_id'] = data_df['company'].map(company_index)

    data_df.drop(columns=['id', 'company'], inplace=True)
    data_df.rename(columns={'origin': 'data_origin'}, inplace=True)

    sqlalchemy_engine = sqlalchemy.create_engine(sqlite.get_sqlalchemy_engine_url())
    for cls in Data1, Data2:
        data_df.loc[cls.__name__.lower()].to_sql(
            name=cls._meta.db_table,
            con=sqlalchemy_engine,
            if_exists='append',
            index=False,
        )
