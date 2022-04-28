from email import quoprimime
import pandas as pd
from pandas import DataFrame

def get_ticker_text(df: DataFrame) -> str:
    '''Format data in DataFrame as a string w/ newline chars and rounded values'''
    new_line = '\n'
    round5_list = [
        'priceChange',
        'lastPrice',
        'openPrice',
        'highPrice',
        'lowPrice',
    ]
    round2_list = [
        'volume',
        'quoteVolume',
    ]
    property_dict = {df[i].name: df[i][0] for i in list(df.keys())[1:]}
    text = f'{df.symbol[0]} info:{new_line}'
    for k, v in property_dict.items():
        if k in round5_list:
            text += f'{new_line}{k}:   {round(float(v), 5)}'
        elif k in round2_list:
            text += f'{new_line}{k}:   {round(float(v), 2)}'
        else:
            text += f'{new_line}{k}:   {v}'

    return text