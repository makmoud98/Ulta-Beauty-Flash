import pandas as pd
import numpy as np

def get_product_by_id(sku_id):
    """Get Product Display Name using a SKU_ID"""
    sku_id = int(sku_id)
    product_catalog = pd.read_csv('static/Product_Catalog.psv', delimiter='|')
    x = product_catalog[product_catalog['SKU_ID'] == sku_id].to_dict(orient='index')
    return x