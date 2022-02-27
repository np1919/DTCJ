import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import pickle


def return_section_labels(df, pickle_loc='outputs/pickled files/Section_Labels.pkl'):
    with open(pickle_loc, 'rb') as f:
        d = pickle.load(f)

    ser = df['COMMODITY_DESC'].map(d) # hardcoded;
    ser = ser.fillna('misc') # for exceptions ?
    return ser