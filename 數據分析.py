#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 16:27:32 2020

@author: kenchiu
"""

import pandas as pd
#房價
house=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/house106.csv',index_col=0)
pplframe=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/pplframe.csv',index_col=0)
birthmarrige=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/birthnmarrige2017.csv',index_col=0)
crimerate=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/crm106rate.csv',index_col=0)
carate=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/carate.csv',index_col=0)
income=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/incomearea106.csv',index_col=0)
education=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/edulevels.csv',index_col=0)

# 
allin1=pplframe.merge(house, left_on=('Area1'), right_on=('鄉鎮市區'),how='outer')
allin1=allin1.merge(birthmarrige, left_on=('Area1'), right_on=('Area'),how='outer')
allin1=allin1.merge(crimerate, left_on=('Area1'), right_on=('location_x'),how='outer')
allin1=allin1.merge(carate, left_on=('Area1'), right_on=('district'),how='outer')
allin1=allin1.merge(income, left_on=('Area1'), right_on=('Area'),how='outer')
allin1=allin1.merge(education, left_on=('Area1'), right_on=('site_id'),how='outer')

allin1=allin1.drop(columns=['Area_x','location_x','district','Area_y'])
allin2=allin1.rename(columns={'交易筆棟數':'houseamount'})
allin2.to_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/allin1.csv')

corelation=allin2.corr(method='pearson')
corelation.to_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/corelation.csv')
#各項整理後的指標合併, 並用函式看皮爾生相關係數

#-----------------------------------------製圖
# 房價
import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt
# 設定製圖參數
font={'family':'PingFang HK','weight':'bold', 'size':'8'}
plt.rc('font',**font)
plt.rc('axes',unicode_minus=False)
plt.rcParams['figure.dpi'] = 300


house=pd.read_csv(r'/Users/kenchiu/Desktop/project/house107.csv',index_col=0)
#直條圖
fig,ax=plt.subplots()
fig.suptitle("房屋交易均價與交易筆數")
ax.set_ylabel("交易均價",color='pink')
ax.tick_params(axis='y',labelcolor='pink')
ax.set_xlabel("District")
ax2= ax.twinx()
ax2.set_ylabel("交易筆數",color='skyblue')
ax2.tick_params(axis='y',labelcolor='skyblue')
house['perm2'].plot(ax=ax, color='pink',kind='bar',align = "edge", width = 0.4)
house['交易筆棟數'].plot(ax=ax2, style='skyblue', kind='bar',align = "edge", width =-0.4)
plt.show()

#散點圖
plt.scatter( house['perm2'],house['交易筆棟數'], c = "g", alpha = 0.5)
plt.ylabel("交易筆數")
plt.xlabel("交易均價")
plt.legend(loc = 4)
plt.show()

#人口概況
import pandas as pd
import matplotlib.pyplot as plt
pplframe=pd.read_csv(r'/Users/kenchiu/Desktop/project/pplframe.csv',index_col=0)
x=pplframe['Area1']
y1=pplframe['km2']
y2=pplframe['ppl']
y3=pplframe['ppldensity']
y4=pplframe['famt']
y5=pplframe['fppl']

plt.bar(x, y1, label = "各區面積", color="g",)
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.legend()
plt.show()

plt.bar(x, y2, label = "人口數",color="red")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.legend()
plt.show()

plt.bar(x, y3, label = "人口密度",color="pink")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.legend()
plt.show()

plt.bar(x, y4, label = "家戶數",color="blue")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.legend()
plt.show()

plt.bar(x, y5, label = "每戶平均人數",color="lightblue")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.ylim(2.0, 3.5)
plt.legend()
plt.show()

plt.scatter(y1, y2, c = "g", alpha = 0.5)
plt.show()

# 地圖
yin=allin2['inrate']
yout=allin2['outrate']
yedu=allin2['eduscore']
yprc=allin2['perm2']

villages_shp = gp.read_file(r'/Users/kenchiu/Desktop/project/TOWN_MOI_1090324.shp', encoding='utf8') #全台灣村里界圖
newT_shp = villages_shp.query('COUNTYNAME=="新北市"') 

allmap= newT_shp.merge(allin2, left_on=('TOWNNAME'), right_on=('Area1'))
allmap.plot(column="ppl", cmap='YlGn', legend=True, 
                 legend_kwds={'label': "population"})

allmap.plot(column="outrate", cmap='Blues', legend=True, 
                 legend_kwds={'label': "遷出率"})

allmap.plot(column="dierate", cmap='Oranges', legend=True, 
                 legend_kwds={'label': "死亡率"})

allmap.plot(column="dincomeperf", cmap='Greens', legend=True, 
                 legend_kwds={'label': "家戶可支配所得"})

allmap.plot(column="eduscore", cmap='Blues', legend=True, 
                 legend_kwds={'label': "平均最高學歷"})


plt.scatter(yin, yout, c = "b", alpha = 0.5)
plt.ylabel("遷出率")
plt.xlabel("遷入率")
plt.show()

plt.scatter(yedu, yprc, c = "b", alpha = 0.5)
plt.ylabel("房屋單位均價")
plt.xlabel("最高學歷")
plt.show()


#家庭概況
import pandas as pd
birthmarrige=pd.read_csv(r'/Users/kenchiu/Desktop/project/birthnmarrige2017.csv',index_col=0)

x=birthmarrige['Area']
y1=birthmarrige['birthrate']
y2=birthmarrige['dierate']
y3=birthmarrige['inrate']
y4=birthmarrige['outrate']
y5=birthmarrige['addrate']
y6=birthmarrige['wedrate']
y7=birthmarrige['dvrcrate']

plt.bar(x, y1, label = "出生率", color="yellowgreen")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.legend()
plt.show()

plt.bar(x, y2, label = "死亡率", color="lightgreen")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.legend()
plt.show()

plt.bar(x, y3, label = "遷入率", color="lightskyblue")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.ylim(20, 120)
plt.legend()
plt.show()

plt.bar(x, y4, label = "遷出率", color="lightblue")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.ylim(30, 90)
plt.legend()
plt.show()

plt.bar(x, y5, label = "社會增加率", color="yellow")
plt.bar((x.min(),x.max()),(0,0),linestyle="-")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.legend()
plt.show()

plt.bar(x, y6, label = "結婚率", color="lightcoral")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.ylim(1.0, 7.5)
plt.legend()
plt.show()

plt.bar(x, y7, label = "離婚率", color="pink")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.ylim(1.0, 3.5)
plt.legend()
plt.show()

# 收入
income=pd.read_csv(r'/Users/kenchiu/Desktop/project/incomearea106.csv',index_col=0)
x=income['district']
y=income['dincomeperf']
a=income['dincomeperf'].mean()
a=str(a.round(2))
avg="平均數:"+a

plt.bar(x, y, label = "家戶可支配所得", color="yellow")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.ylim(600000, 1200000)
plt.text(0.2,1170000,avg)
plt.legend()
plt.show()

# 學歷
education=pd.read_csv(r'/Users/kenchiu/Desktop/project/edulevels.csv',index_col=0)
education.reset_index(drop=False, inplace=True)
x=education['site_id']
y=education['eduscore']
a=education['eduscore'].mean()
a=str(a.round(2))
avg="平均數:"+a

plt.bar(x, y, label = "平均最高學歷", color="cyan")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.ylim(1.5, 3.5)
plt.text(0.1,3.4,avg)
plt.legend()
plt.show()

# 犯罪
crimerate=pd.read_csv(r'/Users/kenchiu/Desktop/project/crm106rate.csv',index_col=0)
x=crimerate['location_x']
y1=crimerate['crmhouse']
y2=crimerate['location_y']
y3=crimerate['crmcar']

plt.bar(x, y1, label = "每萬人房屋竊盜案件", color="coral")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.ylim(0.15, 2.5)
plt.legend()
plt.show()

plt.bar(x, y3, label = "每萬人汽車竊盜案件", color="coral")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.ylim(0.15, 7.5)
plt.legend()
plt.show()

plt.bar(x, y2, label = "每10萬人婦幼犯罪案件", color="coral")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.ylim(0.3, 3.6)
plt.legend()
plt.show()

# 車禍
carate=pd.read_csv(r'/Users/kenchiu/Desktop/project/carate.csv',index_col=0)
x=carate['district']
y=carate['a2hurtppl']

plt.bar(x, y, label = "每萬人車禍發生率(A2)等級", color="coral")
plt.xlabel("District") 
plt.xticks(rotation=90)
plt.ylim(40, 250)
plt.legend()
plt.show()





