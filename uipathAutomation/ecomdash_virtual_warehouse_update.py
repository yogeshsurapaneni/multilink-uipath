import pandas as pd
from datetime import datetime
import sys
import errno

def inventory_update():
    df=pd.read_csv('primaryData.csv')
    finaldf=pd.DataFrame(columns=['SKU Number','Warehouse Quantity'],index=None)

    for i in range(len(df)):

        specialBrands=["Cambium","EnGenius"]
        if df['name'][i].split(' ',2)[0] in specialBrands:
            sku = df['name'][i].split(' ',1)[1].split(' ',2)[1]
        else:
            sku = df['name'][i].split(' ',1)[1].split(' ',2)[0]

        ohioStock=int(df['Stock in Ohio'][i].split(':',1)[1].split(' ',1)[1])
        utahStock=int(df['Stock in Utah'][i].split(':',1)[1].split(' ',1)[1])
        combinedStock=ohioStock+utahStock
        finaldf.loc[i] = [sku,combinedStock]
        i=+1
    #brand=df['name'][0].split(' ',2)[0]
    #str_date_time = datetime.now().strftime("%m%d%Y%H%M%S")
    #finalFile="Reports/"+brand+"_vw_update_"+str_date_time+".csv"
    #finaldf.to_csv(finalFile, index=False)
    return finaldf


inventory_update()
