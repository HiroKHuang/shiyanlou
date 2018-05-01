# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
from pandas import Series, DataFrame

def data_clean():
    df_climate = pd.read_excel('ClimateChange.xlsx', sheet_name='Data')
    df_country = pd.read_excel('ClimateChange.xlsx', sheet_name='Country')
    df_climate = df_climate[df_climate['Series code']=='EN.ATM.CO2E.KT'].set_index('Country code')
    df_climate.drop(labels=['Country name', 'Series code', 'Series name', 'SCALE', 'Decimals'], axis=1, inplace=True)
    df_climate.replace({'..': np.nan}, inplace=True)
    df_climate.fillna(method='ffill', inplace=True)
    df_climate.fillna(method='bfill', inplace=True)
    df_climate.dropna(how='all', inplace=True)
    df_climate['Sum emission'] = df_climate.sum(axis=1)
    df_climate = df_climate['Sum emission']
    df_country.drop(labels=['Capital city', 'Region', 'Lending category'],axis=1,inplace=True) 
    df_country.set_index('Country code', inplace=True)
    return pd.merge(DataFrame(df_climate), df_country, left_index=True,right_index=True)    

def co2():
    data = data_clean()
    df_sum = data['Sum emission'].groupby(data['Income group']).sum()
    df_max = data.sort_values(by='Sum emission',ascending=False).groupby(data['Income group']).head(1).set_index('Income group')
    df_max.columns=['Highest emissions', 'Highest emission country']
    df_max = df_max.reindex(columns=['Highest emission country','Highest emissions'])
    df_min = data.sort_values(by='Sum emission').groupby(data['Income group']).head(1).set_index('Income group')
    df_min.columns = ['Lowest emissions', 'Lowest emission country']
    df_min = df_min.reindex(columns=['Lowest emission country', 'Lowest emissions'])
    result = pd.concat([df_sum, df_max, df_min], axis=1)
    return result
