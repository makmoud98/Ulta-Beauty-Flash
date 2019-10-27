import pandas as pd
import numpy as np

def get_product_name(sku_id):
    """Get Product Display Name using a SKU_ID"""
    sku_id = int(sku_id)
    product_catalog = pd.read_csv('../static/Product_Catalog.psv', delimiter='|')
    return product_catalog[product_catalog['SKU_ID'] == sku_id]['DISPLAY_NAME'].values[0]