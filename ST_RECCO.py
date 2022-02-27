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
# resample_rule = st.sidebar.text_input('Enter Resampling Rule;', value='W')
# always resample on week? month? by average house frequency, given in hh_agg?
# should this class be called household_dashboard?


     #### LOAD SOME DATA #######
transactions = pd.read_csv('data/transaction_data.csv')
product = pd.read_csv('data/product.csv')

     #### CLEAN THE DATA
transactions.drop(transactions[transactions['QUANTITY'] ==0].index)
product['Section Labels'] = my_funcs.return_section_labels(product)


    #### MERGE THE DATA
df = transactions.merge(product[['PRODUCT_ID', 'COMMODITY_DESC', 'Section Labels']])

    #### CACHE THE LABELED AND DATED DF #####
@st.cache # hopefully this saves the final df for reference in the class call.
def merged():
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
               
        

        ### CALLING THE FUNCTION
# st.write(recco_wrapper(household_choice).__dict__)
st.write(recco_wrapper(household_choice).df)






# @st.cache
# def get_data(hh_key):
#     transactions = pd.read_csv('data/transaction_data.csv')
#     transactions.drop(transactions[transactions['QUANTITY'] ==0].index)
#     my_funcs.add_datetime(transactions)
#     product = pd.read_csv('data/product.csv')
#     merged = transactions.merge(product[['PRODUCT_ID', 'COMMODITY_DESC', 'SUB_COMMODITY_DESC']])
#     merged['Section Labels'] = my_funcs.return_section_labels(merged)
    
#     return merged[merged['household_key'] == hh_key]


# # st.dataframe(get_data(choice))
# st.write(f"{get_data(choice)['BASKET_ID'].nunique()} baskets for Household {choice}")
# st.write(f"{get_data(choice)['PRODUCT_ID'].nunique()} Unique Products over {get_data(choice).shape[0]} Rows")


# resampled = get_data(choice).set_index('datetime').resample(rule=resample_rule)['SALES_VALUE'].sum()

# fig, ax = plt.subplots(figsize=(16,6))
# plt.title(f'{resample_rule}-resampled Sales for Household {choice}', size=16)
# ax.plot(resampled)
# ax.axhline(resampled.mean(), ls='--', color='orange', label=f'Avg. {resample_rule} Sales : {resampled.mean()}')
# plt.legend()
# st.pyplot(fig)