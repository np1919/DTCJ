import datetime
import numpy as np
import pandas as pd

def section_labels() -> dict:
    with open('Section_Labels.txt', 'r') as f:
        d = eval(f.read())
        return d
type(section_labels())

def return_section_labels(df) -> pd.Series:
    #hardcoded map
    d = section_labels()
    # map the dictionary to the Series using the .map() method of the pd.Series class
    ser = df['COMMODITY_DESC'].map(d)
    # in case of improper transactions..
#     ser = ser.fillna('misc') # leave off?
    ser.name = 'Section Labels'
    return ser

# return_section_labels(merged)

def get_section_sales(df) -> pd.DataFrame():
    
    idx = df.index
    # get dummies for each transaction row
    section_dummies = pd.get_dummies(df['Section Labels'])

    # multiply each row by it's SALES VALUE
    section_sales = section_dummies.apply(lambda x: x * df['SALES_VALUE'])
#     print(all(section_sales.index == idx))
    # add and group by household key, sum all rows from the dummy columns
    section_sales = section_sales.join(df[['household_key']]).groupby('household_key').agg(sum)
    return section_sales
