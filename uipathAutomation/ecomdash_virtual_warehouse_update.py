import shutil

import pandas as pd
from datetime import datetime, date, timedelta
import os
import re

def cleanReports():
    yesterdaydate = (date.today() - timedelta(days=1)).strftime('%m%d%Y')
    if os.path.exists("Reports/"+yesterdaydate):
        shutil.rmtree("Reports/"+yesterdaydate)
def inventory_update():
    df=pd.read_csv('primaryData.csv')
    finaldf=pd.DataFrame(columns=['SKU Number','Warehouse Quantity'],index=None)
    for i in range(len(df)):
        specialBrands=["EnGenius","Grandstream","Mimosa","RF","Ubiquiti","Shireen"]
        if df['name'][i].split(' ',2)[0] in specialBrands:
            sku = df['name'][i].split(' ',1)[1].split(' ',2)[1]
        else:
            sku = df['name'][i].split(' ',1)[1].split(' ',2)[0]

        notToUpdateSKU = ["CRS309-1G-8S+IN"]
        if sku in notToUpdateSKU:
            continue

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
        if combinedStock >= 100:
            cappedStock=100
        else:
            cappedStock=combinedStock
        finaldf.loc[i] = [sku,cappedStock]
        i=+1
    brand=df['name'][0].split(' ',2)[0]
    date=datetime.now().strftime("%m%d%Y")
    isExist = os.path.exists("Reports/"+date)
    if not isExist:
        os.makedirs("Reports/"+date)
    finalFile="Reports/"+date+"/"+brand+"_vw_update.csv"
    finaldf.to_csv(finalFile, index=False)
    if df['name'][i].split(' ', 2)[0] == "MikroTik":
        inventory_update_withPrice()
def inventory_update_withPrice():
    df=pd.read_csv('primaryData.csv')
    finaldf=pd.DataFrame(columns=['SKU Number','Warehouse Quantity','Cost'],index=None)

    for i in range(len(df)):
        specialBrands=["EnGenius","Grandstream","Mimosa","RF","Ubiquiti","Shireen"]
        if df['name'][i].split(' ',2)[0] in specialBrands:
            sku = df['name'][i].split(' ',1)[1].split(' ',2)[1]
        else:
            sku = df['name'][i].split(' ',1)[1].split(' ',2)[0]

        notToUpdateSKU = ["CRS309-1G-8S+IN"]
        if sku in notToUpdateSKU:
            continue

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
        if combinedStock >= 100:
            cappedStock=100
        else:
            cappedStock=combinedStock
        cost=df['Price'][i].replace("$", '')
        finaldf.loc[i] = [sku,cappedStock,cost]
        i=+1
    brand=df['name'][0].split(' ',2)[0]
    date=datetime.now().strftime("%m%d%Y")
    isExist = os.path.exists("Reports/"+date)
    if not isExist:
        os.makedirs("Reports/"+date)
    finalFile="Reports/"+date+"/"+brand+"_vw_update_with_price.csv"
    finaldf.to_csv(finalFile, index=False)

cleanReports()
inventory_update()