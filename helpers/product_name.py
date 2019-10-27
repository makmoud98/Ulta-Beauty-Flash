import pandas as pd
import numpy as np
import cloudinary
import cloudinary.uploader
import cloudinary.api
import pickle

sku_to_image = pd.read_csv('static/sku_to_img.csv')
product_catalog = pd.read_csv('static/Product_Catalog.psv', delimiter='|')

def get_product_img_url(sku_id):
    url = sku_to_image[sku_to_image['SKU_ID'] == int(sku_id)]['img_url'].values[0]
    x = cloudinary.uploader.upload(url,crop="limit",tags="samples",width=100,height=100)
    return x['secure_url']

def get_product_tojson(sku_id):
    """Get Product Display Name using a SKU_ID"""
    sku_id = int(sku_id)
    row = product_catalog[product_catalog['SKU_ID'] == sku_id]
    row = row.transpose().to_dict()
    key = list(row.keys())[0]
    row[key]['img_url'] = get_product_img_url(sku_id)
    return row[key]

def get_product(sku_id):
    """Get Product Display Name using a SKU_ID"""
    sku_id = int(sku_id)
    row = product_catalog[product_catalog['SKU_ID'] == sku_id]
    return row