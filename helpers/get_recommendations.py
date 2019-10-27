import numpy as np
import pandas as pd

def get_most_popular():
    """Function that returns the most popular items"""
    utility = pd.read_csv('../static/utility_matrix.csv')
    total_purchases = utility.sum(axis=0)
    sorted_purchases = sorted(range(len(total_purchases)), key=lambda k: total_purchases[k], reverse=True)[1:]
    return utility.columns[sorted_purchases[:5]].tolist()