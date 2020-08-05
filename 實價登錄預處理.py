#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 15:34:53 2020

"""


# 房價106
import pandas as pd
# import geopandas as gp
houses061=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/F_lvr_land_A106S1.csv',
                    index_col=1,usecols=[0,1,8,22])
houses062=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/F_lvr_land_A106S2.csv',
                    index_col=1,usecols=[0,1,8,22])
houses063=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/F_lvr_land_A106S3.csv',
                    index_col=1,usecols=[0,1,8,22])
houses064=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/F_lvr_land_A106S4.csv',
                    index_col=1,usecols=[0,1,8,22])

houses061.reset_index(drop=False, inplace=True) 
houses061=houses061.drop(index=0,axis=0)
houses062.reset_index(drop=False, inplace=True) 
houses062=houses062.drop(index=0,axis=0)
houses063.reset_index(drop=False, inplace=True) 
houses063=houses063.drop(index=0,axis=0)
houses064.reset_index(drop=False, inplace=True) 
houses064=houses064.drop(index=0,axis=0)

housesall06=pd.concat([houses061,houses062,houses063,houses064])
housesall06.reset_index(drop=True, inplace=True) 

# 計算各區交易筆數
housesallcount6=housesall06.groupby("鄉鎮市區").count() # 各區交易筆數（建物土地車位皆計算）
housecount6=housesallcount6.drop(columns=['單價元平方公尺','交易標的'])
# 計算各區交易均價, 移除僅有土地與車位的交易, 確認單價計算皆含有建物
housesall06['交易筆棟數＿建物']=housesall06['交易筆棟數'].apply(lambda x: x[3:6]) 
houseallmsk=housesall06['交易筆棟數＿建物']!="建物0"
houseallbuild=housesall06[houseallmsk]
houseallbuildprice=houseallbuild.drop(columns=['交易筆棟數＿建物','交易筆棟數','交易標的'])
houseallbuildprice['perm2']=houseallbuildprice['單價元平方公尺'].astype('float64') 
hallper=houseallbuildprice.drop(columns="單價元平方公尺")
hallperavg06=hallper.groupby("鄉鎮市區").mean()  # 各區交易均價

# 存成一張以區域分類的交易筆數與交易均價數值表
houseall106=hallperavg06.merge(housecount6,left_on="鄉鎮市區", right_on="鄉鎮市區", how='outer')
houseall106.to_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/house106.csv')

#================================================================================
'''
還沒改
'''
import geopandas as gp
# 圖像化, 用geopandas畫出地圖
villages_shp = gp.read_file(r'/Users/kenchiu/Desktop/project/TOWN_MOI_1090324.shp', 
                            encoding='utf8') #全台灣村里界圖
newT_shp = villages_shp.query('COUNTYNAME=="新北市"') 

houseprcmap= newT_shp.merge(houseall106, left_on=('TOWNNAME'), right_on=('鄉鎮市區'))
houseprcmap.plot(column="perm2", cmap='OrRd', legend=True, 
                 legend_kwds={'label': "average price per square meter"})
houseprcmap.plot(column="交易筆棟數", cmap='OrRd', legend=True,
                 legend_kwds={'label': "trade case by district"})




