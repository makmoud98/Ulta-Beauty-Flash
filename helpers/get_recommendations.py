import numpy as np
import pandas as pd
from helpers.product_name import get_product_by_id

utility = pd.read_csv('static/utility_matrix.csv')

def get_most_popular():
    """Function that returns the most popular items"""
    total_purchases = utility.sum(axis=0)
    sorted_purchases = sorted(range(len(total_purchases)), key=lambda k: total_purchases[k], reverse=True)[1:]
    items = list(map(lambda x: get_product_by_id(x), utility.columns[sorted_purchases[:5]].tolist()))
    return items

def get_product_recommendations(keyword):
	return []