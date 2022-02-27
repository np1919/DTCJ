import streamlit as st
import pickle
import pandas as pd
import my_funcs as mf

## This Script is to be run using the `streamlit run [FILENAME]` command
## the st.cache decorator allows us to store the results of a given function.
## Passing new arguments (to the same function) will result in a new function call.
# @st.cache
# def load_df(path='data/product.csv'): # transactions is ~250MB which exceeds 50MB limit.
#     df = pd.read_csv(path) # product.csv LOADS~!! almost 100k rows * 7!!!
#     return df


# df = load_df() # function call executes
# df



"## I'd like to operationalize the recommender system I created in Jupyter Notebooks"
"With some number of cluster labels (which define customers)..have a support table for each kind?"

# Something like...

## have a pickle file for each household's transactions.
    # pick a household
    # check the transactions. 
@st.cache
def load_hh_transactions(choice):
    df = pd.read_csv('data/transaction_data.csv')
    return df[df['household_key'] == choice]

hh1 = load_hh_transactions(1)

hh1