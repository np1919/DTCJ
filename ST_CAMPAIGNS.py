import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import my_funcs as mf
import numpy as np

# TODO: Edit the add_datetime function to import the map from a pickle file, and that's it.

choice = st.sidebar.slider('Pick a Campaign', 1,31)
f'# Campaign {choice}'


@st.cache
def load_campaign_dict():
    with open('campaign_summary.pkl', 'rb') as f:
        mydict = pickle.load(f)
    return mydict

### Proof of SPEED
# for camp_no in mydict.keys():
#     for key in mydict[camp_no].keys():
#         f"The {key} of campaign {camp_no} {mydict[camp_no][key]}"

@st.cache
def load_campaign_sales(camp_no, mydict):
    
    # cache these results in a pickle file....
    transactions = pd.read_csv('data/transaction_data.csv')
    transactions = transactions[transactions['DAY']>100]
    products = pd.read_csv('data/product.csv')
    product_list = mydict[camp_no]['Listed Products']
    sliced_trans = transactions[transactions['PRODUCT_ID'].isin(product_list)]
    products['Section Labels'] = mf.return_section_labels(products)
    mf.add_datetime(sliced_trans)                                                           
    sliced_merged = sliced_trans.merge(products.drop('CURR_SIZE_OF_PRODUCT', axis=1))    
    return sliced_merged



def plot_campaign_sales(camp_no, my_dict):

    merged = load_campaign_sales(camp_no, my_dict)
    fig, ax = plt.subplots(figsize=(32,12))
    
    plt.title(f'Sales for Products in Campaign {camp_no}')
    plt.ylabel(f'Avg. Daily Sales')
    plt.xlabel('DAY')    
    
    first = mydict[camp_no]['First Day']
    last = mydict[camp_no]['Last Day']
    total_days = mydict[camp_no]['Duration']
    
    ### How Much Data
    trans_max = merged['DAY'].max()
    trans_min = merged['DAY'].min()

    ax.plot(merged.groupby('DAY')['SALES_VALUE'].sum(), color='black', label=' Listed Products Sales')
    plt.axvspan(first, last, alpha=0.2, color='yellow')

    val = mydict[camp_no]['Listed Products Sales During'] / (last - first) + 1
    ax.plot((first, last), (val, val) , color='red', lw=3, ls='--', label=f'Avg. during {round(val,2)}')

    val = mydict[camp_no]['Listed Products Sales After'] / (trans_max - last) + 1
    ax.plot((last, trans_max), (val, val) , color='blue', lw=3, ls='--', label=f'Avg. after {round(val,2)}')

    val = mydict[camp_no]['Listed Products Sales Before'] / (first - trans_min) + 1 
    ax.plot((trans_min, first), (val, val) , color='purple', lw=3, ls='--', label=f'Avg. before {round(val,2)}')

#     val = mydict[camp_no]['Listed Products Total Sales'] / ((trans_max - trans_min) +1)
#     ax.plot((trans_min, trans_max), (val, val) , color='cyan', lw=3, ls='-', label=f'Avg. total {round(val,2)}', alpha=0.5)
    plt.legend()
    
    ### PLOTTING
    st.pyplot(fig, clear_figure=True)
    
### RUNTIME if __name__ == '__main__':

mydict = load_campaign_dict()
merged = load_campaign_sales(choice, mydict)
plot_campaign_sales(choice, mydict)
# st.dataframe(data=mydict[choice])



### NOTES ###

#     ### Plotting...
# fig, ax = plt.subplots()
# ax.plot(sales_Series.groupby('DAY')['SALES_VALUE'].sum())
# st.pyplot(fig, clear_figure=True)
