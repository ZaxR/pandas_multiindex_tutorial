import itertools

import numpy as np
import pandas as pd


def mock(upc):
    rand_dates = np.random.choice(dates, np.random.randint(4, len(dates)), replace=False)
    rand_stores = np.random.choice(stores, np.random.randint(2, len(stores)), replace=False)

    return list(itertools.product(*[rand_dates, rand_stores, [upc]]))


if __name__ == '__main__':
    dates = ['7/10/18', '7/11/18', '7/12/18', '7/13/18', '7/14/18', '7/15/18', '7/16/18']
    stores = ['Store 1', 'Store 2', 'Store 3']
    upc_meta_data = pd.read_csv('upc_meta_data.csv', dtype={'UPC EAN': str})

    to_concat = []
    for upc in upc_meta_data['UPC EAN']:
        tdf = pd.DataFrame(mock(upc), columns=['Date', 'Store', 'UPC EAN'])
        tdf = tdf.merge(upc_meta_data[upc_meta_data['UPC EAN'] == upc], how='left', on='UPC EAN')
        tdf['Units'] = np.random.randint(4, 15, tdf.shape[0])
        tdf['Dollars'] = (tdf['Units']
                          * np.round(np.random.uniform(tdf['Price Low'], tdf['Price High'], tdf.shape[0]), 2))
        tdf.drop(columns=['Price Low', 'Price High'], inplace=True)

        to_concat.append(tdf)

    df = pd.concat(to_concat)
    df = df[['Date', 'Store', 'Category', 'Subcategory', 'UPC EAN', 'Description', 'Dollars', 'Units']]
    df.to_csv('data.csv', index=None)
