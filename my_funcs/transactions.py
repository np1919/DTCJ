import datetime
import pandas as pd
import numpy as np
import my_funcs

def load_merged(trans=None, prod=None) -> pd.DataFrame():
    if not trans:
        trans = pd.read_csv('data/transaction_data.csv')
        
    if not prod:
        prod = pd.read_csv('data/product.csv')
   

    trans['datetime'] = my_funcs.add_datetime(trans)
#     prod['Section Labels'] = my_funcs.return_section_labels(products)
    
    # Remove Empty Sales Rows
    trans = trans[(trans['QUANTITY'] > 0) & 
                  (trans['SALES_VALUE'] > 0)]

    
    # Remove monthly/quarterly tails...
    trans = trans[(trans['datetime'] >= "2004-7-1") &
                  (trans['datetime'] < "2006-3-1")]
    
                   
    # Merge
    merged = trans.merge(prod.drop('CURR_SIZE_OF_PRODUCT', axis=1))
    
    # Remove Gasoline Sales
    merged.drop(merged[merged['SUB_COMMODITY_DESC']=='GASOLINE-REG UNLEADED'].index, axis=0, inplace=True)
    merged.drop(merged[merged['COMMODITY_DESC']=='GASOLINE-REG UNLEADED'].index, axis=0, inplace=True)
    
    merged['Section Labels'] = my_funcs.return_section_labels(merged)
    
    def one_day_transactions(df) -> list:
        no_days = df.groupby('household_key').agg({'DAY':'nunique'})
        return list(no_days[no_days['DAY'] == 1].index)
        
    # remove households with only 1 day of purchases;
    merged = merged[~merged['household_key'].isin(one_day_transactions(merged))]    
    return merged

def make_date_map(df, last_day_column) -> dict:
    '''return a dictionary '''
    # 'DAY' 1 == 2004-03-23
    day1 = datetime.datetime(2004, 3, 23) # as derived in transactions notebook; datetime for 'DAY' == 1
    ineedthismany = df[last_day_column].max()
    last = day1 + datetime.timedelta(days=int(ineedthismany)- 1)   
    date_range = pd.date_range(day1, last) # date range for our data
    # map datetime index to DAY; enumerate() indexes from 0, so we add 1
    date_map = {i+1:x for i, x in enumerate(date_range)}

    output = df[last_day_column].map(date_map)
    output = pd.to_datetime(output)
    return date_map

def days_between(df):
    '''take the .diff() of the sorted list of transaction dates for each household;
    round the mean of that and return a Series of all households in df
    '''
    days_between = dict()
    # loop through household_keys
    for key in df['household_key'].unique():

        # find the subset of transactions matching that household and  use .diff() to calculate the days between...
        # ...transactions; multiple transactions on the same day are ignored.
        a = pd.Series(df[df['household_key']==key]['DAY'].unique()).sort_values().diff()[1:]

        #calculate the mean difference between days of purchase
        days_between[key] = round(a.mean(), 2)


    ser = pd.Series(data=days_between.values(), index=days_between.keys())
#     ser.name = 'days_between_purchases'
    ser = pd.DataFrame(ser).reset_index()
    ser.columns=['household_key', 'days_between_purchases']
    return ser # included in the huge function below