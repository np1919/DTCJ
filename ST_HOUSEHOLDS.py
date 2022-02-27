import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import my_funcs as mf
import numpy as np
import datetime

from itertools import cycle
colors = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'][-3:])

### HOUSEHOLD DASHBOARDS
### implemented on streamlit

#### THOUGHTS:
# Allow the user to switch between campaigns and household dashboards? What about customer labels; the different `support` groups?

### USER INPUT
    # - resample rule
    # - household

choice = st.number_input('Pick a Household', 1, 2500) # this must be an integer between 1 and 2500..?
st.write(f'# Household {int(choice)}')
resample_rule = st.text_input('Pick a resample rule', 'BM')


## LOADING DATA FROM /OUTPUTS/
#  - hh_targeted (not accounted for)
# - campaign summary
# - hh_sales (individual table for each 'hh' transaction)

# fallback loads
    # merged = pd.read_csv('outputs/merged.csv')
    # merged['datetime'] = pd.to_datetime(merged['datetime'])

# LOADING DATES (for all campaigns)
with open('outputs/hh_targeted.txt', 'r') as f:
    hh_targeted = dict(eval(f.read()))
    
# LOADING CAMPAIGN REFERENCE TABLE
campaign_summary = pd.read_csv('outputs/campaign_summary.csv', index_col=0).T
    
# CACHE FOR LOADING HOUSEHOLD SALES DATA

@st.cache
def load_household_sales(hh_key):           
    df = pd.read_csv(f'outputs/hh_sales/hh{int(hh_key)}_sales.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])

    return df



#### FUNCTIONALITY

## as long as `groups` exists in df:
## group df by groups; resample by `resample_rule`
## plot the ['SALES_VALUE'] of each group, over time

def plot_section_sales(df, 
                        resample_rule='BM', 
                        groups='Section Labels',
                         dt_col='datetime',
                          sales_col='SALES_VALUE',
                          ):
    # iterate through each available section
    fig, ax = plt.subplots(figsize=(32,12))
    plt.title(f'Sales for Household {int(choice)}', fontsize=50)
    plt.ylabel(f'Sales by {resample_rule}', fontsize=30)
    plt.xlabel('Time', fontsize=30)    
    plt.xticks(fontsize=30, rotation=45)
    plt.yticks(fontsize=30)
    for section in df[groups].unique():
        # plot the graph
        ax.plot(df[df[groups] == section].resample(rule=resample_rule, on=dt_col,)[sales_col].sum(),
                 label=f'{section}',)
        

        ### it's shading the campaigns. This should be a separate function, somehow implemented on the same st.pyplot call.
        ### references `hh_targeted` to plot campaigns. They should have different colours; and hopefully labels!
        ## 

    def plot_campaign_spans(choice=choice):
        campaign_labels = [x for x in hh_targeted[int(choice)].keys()]
        campaign_colors = []
        for campaign in campaign_labels:
            first, last = hh_targeted[int(choice)][int(campaign)]
            campaign_color = next(colors)
            campaign_colors.append(campaign_color)
            ax.axvspan(first, last, alpha=0.3, color=campaign_color)
        
            ### TODO: add colours, labels; ## cycle function? color wheel? ## zip ## campaign number ## change legend (labels, color?)
        
    plot_campaign_spans()
    plt.legend(fontsize=30)
    
    ### PLOTTING
    st.pyplot(fig)
 

def plot_household_sales(hh_key, 
                        resample_rule='D', 
                        dt_col='datetime',
                        sales_col='SALES_VALUE',
                        ):
    # grabbing the data for hh_key
    df = load_household_sales(hh_key)
    # resampling to create sales series
    sales = df.resample(resample_rule, on=dt_col)[sales_col].sum()
    # plotting
    fig, ax = plt.subplots(figsize=(32,12))
    plt.title(f'Sales for Household {int(choice)}')
    plt.ylabel(f'Sales by {resample_rule}')
    plt.xlabel('Time')    
    ax.plot(sales, color='black', label='Household Sales')
    plt.legend()
    
    
    
    ### PLOTTING
    st.pyplot(fig, clear_figure=True)
    
### RUNTIME
# plot the chart for the household
# plot_household_sales(load_household_sales(choice), resample_rule)
plot_section_sales(load_household_sales(choice), resample_rule)

### List campaigns the household was targeted by, with their dates
st.markdown('## Campaigns this Household was Targeted by:')
for campaign in hh_targeted[int(choice)].keys():
    first, last = hh_targeted[int(choice)][int(campaign)]
    st.write(campaign, first, last)
    st.write(campaign_summary[campaign]['Section Label Counts'])
    