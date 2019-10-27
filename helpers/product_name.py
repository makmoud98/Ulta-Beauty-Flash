import pandas as pd
import numpy as np
import cloudinary
import cloudinary.uploader
import cloudinary.api
sku_to_image = pd.read_csv('static/sku_to_img.csv')

def get_product_img_url(sku_id):
    sku_url = sku_to_image[sku_to_image['SKU_ID'] == int(sku_id)].to_dict()
    url_id = list(sku_url['img_url'].keys())[0]
    url = sku_url['img_url'][url_id]
    print(url)
    x = cloudinary.uploader.upload(url,crop="limit",tags="samples",width=100,height=100)
    return x['secure_url']

product_catalog = pd.read_csv('static/Product_Catalog.psv', delimiter='|')
def get_product_by_id(sku_id):
    """Get Product Display Name using a SKU_ID"""
    sku_id = int(sku_id)
    x = product_catalog[product_catalog['SKU_ID'] == sku_id].to_dict(orient='index')
    
    x[list(x.keys())[0]]['img_url'] = get_product_img_url(sku_id)
    print(x)
    return x