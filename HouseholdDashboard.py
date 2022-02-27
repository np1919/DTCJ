import streamlit as st
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import my_funcs
import my_funcs.end as mfe

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import fpgrowth

#### allow recommendations for any household in the data. 
    # Plot their spending by section, over time 
    # TODO: add in their hh_agg Series... 
    
    
    ### CHOOSE A HOUSEHOLD #### 
household_choice = st.sidebar.number_input('Choose Household Key', value=1)
resample_rule = st.sidebar.text_input('Enter Resampling Rule;', value='W')
# always resample on week? month? by average house frequency, given in hh_agg?
# should this class be called household_dashboard?


 

    #### CACHE THE LOADED, CLEANED, LABELED, DATED AND MERGED #####
@st.cache 
def merged():
            #### LOAD SOME DATA #######
    transactions = pd.read_csv('data/transaction_data.csv')
    product = pd.read_csv('data/product.csv')
         #### CLEAN THE DATA
    transactions.drop(transactions[transactions['QUANTITY'] ==0].index)
           ### LABEL THE DATA
    product['Section Labels'] = my_funcs.return_section_labels(product)
           #### DATE THE DATA
    my_funcs.add_datetime(transactions)
        #### MERGE THE DATA
    df = transactions.merge(product[['PRODUCT_ID', 'COMMODITY_DESC', 'Section Labels']])

    return df


    #### CALL THE RECOMMENDER ON THE HOUSEHOLD ####

@st.cache
def recco_wrapper(household_choice):
    return mfe.RecommenderSystem(
                 household_choice,   ### FOR HOUSEHOLDS#!### 
                 df=merged(), 
                 column='COMMODITY_DESC', 
                 max_len=None, ### CONSIDER REDUCING THIS VALUE FOR SIMPLICITY ###
                 support_threshold=0.05, ### WITH DATA OF FIXED SIZE, NOT A CONCERN? ###
                 metric='confidence', 
                 assoc_threshold=0.8,)
               


        ### CACHE-ING DASHBOARD FOR A CHOICE
@st.cache
def plot_household_sales(recco_object_df, resample_rule):
    fig, ax = plt.subplots(figsize=(45,15))
    plt.title(f'{resample_rule} Transactions for Household {int(household_choice)}', size=24)
    plt.ylabel(f'Sales Value')
    plt.xlabel(f'Datetime')    

    
    sales_series = recco_object_df.set_index('datetime').resample(rule=resample_rule)['SALES_VALUE'].sum()
    ax.plot(sales_series, color='black', label=f'Household Sales by {resample_rule}')
    ax.axhline(sales_series.mean(), color='red', lw=4, label=f'Mean Sales; {sales_series.mean()}')
    
    plt.legend()
    
    ### PLOTTING
    st.pyplot(fig)

    
    
#### IF NAME == MAIN
# plot_household_sales(recco_wrapper(household_choice).df, resample_rule)
most_bought = recco_wrapper(household_choice).df['COMMODITY_DESC'].value_counts()[:5].index

st.write(f'The top 5 most-purchased items for this household were:')
for x in most_bought:
    st.write(x, end='\n')

reccos = recco_wrapper(household_choice).assoc_table.sort_values('lift', ascending=False)[['antecedents', 'consequents']].values[:5]

st.write(f'Recommendations: ')
for x in reccos:
    st.write(str(x), end='\n')



