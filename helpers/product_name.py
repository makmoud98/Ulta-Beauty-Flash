import pandas as pd
import numpy as np
import cloudinary
import cloudinary.uploader
import cloudinary.api

def get_product_img(sku_id):
	x = cloudinary.uploader.upload("https://avatars2.githubusercontent.com/u/8992468",crop="limit",tags="samples",width=100,height=100)
	print(x)
	return x

def get_product_by_id(sku_id):
    """Get Product Display Name using a SKU_ID"""
    sku_id = int(sku_id)
    product_catalog = pd.read_csv('static/Product_Catalog.psv', delimiter='|')
    x = product_catalog[product_catalog['SKU_ID'] == sku_id].to_dict(orient='index')
    return x