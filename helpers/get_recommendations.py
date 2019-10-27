import numpy as np
import pandas as pd
from helpers.product_name import get_product_tojson

utility = pd.read_csv('static/utility_matrix.csv')


def get_most_popular():
    """Function that returns the most popular items"""
    total_purchases = utility.sum(axis=0)[1:]
    indices = list(map(int, total_purchases.index.tolist()))
    total_purchases = [(indices[i], x) for i, x in enumerate(total_purchases)]
    total_purchases = sorted(
        total_purchases, key=lambda x: x[-1], reverse=True)
    top = total_purchases[:5]

    items = [get_product_tojson(x[0]) for x in top]
    return items


user_recs = open('../static/user_recs.txt')
user_hist = open('../static/user_history.txt')
category_array = open('../static/categories.txt')

lst_recs = eval(user_recs.read())
category_array = eval(category_array.read())
lst_recs = lst_recs[0]
hist = eval(user_hist.read())

user_recs.close()
user_hist.close()

def find_top_n(lst, n):
    lst = [x[-1] for x in lst] # remove tups 
    choices = np.random.choice(lst, n)
    # remove dups 
    choices = set(choices) 
    choices = list(choices)
    return choices

def find_keyword(keyword):
    index = category_array.index(keyword)
    return lst_recs[index]

def get_product_recommendations(keyword, n=5):
    lst = keyword.lower().split(' ')
    if len(lst) > 1 and keyword not in category_array:
        if ('face' in lst):
            keyword = 'face masks'
        if ('brushes' in lst):
            keyword = 'makeup brushes'
        if ('hair' in lst):
            keyword = 'oils and serums'
        if ('eyes' in lst):
            keyword = 'eyeshadow'
        if ('cream' in lst):
            keyword = 'hand cream and foot cream'

    try:
        keyword_lst = find_keyword(keyword)
        sku_lst = find_top_n(keyword_lst, n)
        items = [get_product_tojson(x) for x in sku_lst]
    except Exception:
        items = get_most_popular()
    return items
