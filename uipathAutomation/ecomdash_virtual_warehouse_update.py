import pandas as pd
from datetime import datetime
import os
import re

def inventory_update():
    df=pd.read_csv('primaryData.csv', on_bad_lines='skip')
    finaldf=pd.DataFrame(columns=['SKU Number','Warehouse Quantity'],index=None)

    for i in range(len(df)):
        specialBrands=["EnGenius","Grandstream","Mimosa","RF","Ubiquiti"]
        if df['name'][i].split(' ',2)[0] in specialBrands:
            sku = df['name'][i].split(' ',1)[1].split(' ',2)[1]
        else:
            sku = df['name'][i].split(' ',1)[1].split(' ',2)[0]


        if str(df['Stock in Ohio'][i]) == 'nan':
            ohioStock=0
        else:
            if df['Stock in Ohio'][i].count('\n') >= 1:
                lines=df['Stock in Ohio'][i].split('\n')
                if ',' in lines[0].split(':',1)[1].split(' ',1)[1]:
                    ohioStock = int(re.sub(",", "", lines[0].split(':',1)[1].split(' ',1)[1]))
                else:
                    ohioStock = int(lines[0].split(':',1)[1].split(' ',1)[1])
            else:
                if ',' in df['Stock in Ohio'][i].split(':',1)[1].split(' ',1)[1]:
                    ohioStock = int(re.sub(",", "", df['Stock in Ohio'][i].split(':',1)[1].split(' ',1)[1]))
                else:
                    ohioStock = int(df['Stock in Ohio'][i].split(':',1)[1].split(' ',1)[1])

        if str(df['Stock in Utah'][i]) == 'nan':
            utahStock=0
        else:
            if df['Stock in Utah'][i].count('\n') >= 1:
                lines=df['Stock in Utah'][i].split('\n')
                if ',' in lines[0].split(':',1)[1].split(' ',1)[1]:
                    utahStock = int(re.sub(",", "", lines[0].split(':',1)[1].split(' ',1)[1]))
                else:
                    utahStock = int(lines[0].split(':',1)[1].split(' ',1)[1])
            else:
                if ',' in df['Stock in Utah'][i].split(':',1)[1].split(' ',1)[1]:
                    utahStock = int(re.sub(",", "", df['Stock in Utah'][i].split(':',1)[1].split(' ',1)[1]))
                else:
                    utahStock = int(df['Stock in Utah'][i].split(':',1)[1].split(' ',1)[1])

        combinedStock=ohioStock+utahStock
        finaldf.loc[i] = [sku,combinedStock]
        i=+1
    brand=df['name'][0].split(' ',2)[0]
    date=datetime.now().strftime("%m%d%Y")
    isExist = os.path.exists("Reports/"+date)
    if not isExist:
        os.makedirs("Reports/"+date)
    finalFile="Reports/"+date+"/"+brand+"_vw_update.csv"
    finaldf.to_csv(finalFile, index=False)

inventory_update()
