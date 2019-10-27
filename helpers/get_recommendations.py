import numpy as np
import pandas as pd
from helpers.product_name import get_product_tojson

utility = pd.read_csv('static/utility_matrix.csv')

def get_most_popular():
    """Function that returns the most popular items"""
    total_purchases = utility.sum(axis=0)[1:]
    indices = list(map(int, total_purchases.index.tolist()))
    total_purchases = [(indices[i], x) for i, x in enumerate(total_purchases)] 
    total_purchases = sorted(total_purchases, key = lambda x: x[-1], reverse = True) 
    top = total_purchases[:5]

    items = [get_product_tojson(x[0]) for x in top]
    return items

def get_product_recommendations(keyword):
	return []