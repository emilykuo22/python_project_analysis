# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# 資料分析實作
import pandas as pd
# 人口數與密度處理
#Field1(年)、Field2(新北市及行政區別)、Field3(土地面積_平方公里_)、Field6(現住戶數)
#Field7(現住人口數)、Field10(戶量_人除以戶_)、Field11(人口密度_人除以平方公里_)

p=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/現住戶數、人口密度及性比例_000.csv',
              index_col=0, usecols=[0,1,2,5,6,9,10])
w=p.tail(30)
x=w.rename({"TEP_ID":"TEP_Count","Field2":"Area1","Field3":"km2",
            "Field6":"famt","Field7":"ppl","Field10":"fppl","Field11":"ppldensity"}, 
           axis='columns')
x.reset_index(drop=False, inplace=True)
y=x.drop(columns='Field1')
y=y.drop(y.index[0],axis=0)
# 整理新北各區人口概況並存成資料表
y.to_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/pplframe.csv')

#---------------------------------------------------------------------------------

# 出生與離婚率
# Field1(年)、Field2(新北市及行政區別)、Field42(粗出生率)、Field46(粗死亡率)、
# Field48(遷入率)、Field49(遷出率)、Field50(社會增加率)、Field51(結婚對數)、Field52(結婚率)、
# Field53(離婚對數)、Field54(離婚率)
import pandas as pd
marrige=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/戶籍動態_0008126373116681873205.csv',
                    index_col=0, usecols=[0,1,41,45,47,48,49,50,51,52,53])
a=marrige.drop(marrige.index[1:552])
b=a.rename({"Field2":"Area","Field42":"birthrate","Field46":"dierate",
            "Field48":"inrate","Field49":"outrate","Field50":"addrate","Field51":"wed",
            "Field52":"wedrate","Field53":"dvrc","Field54":"dvrcrate"}, axis='columns')
b.reset_index(drop=True, inplace=True) 
c=b.drop(b.index[0],axis=0)
d29=pd.Series(c['Area']) #另抓出區域索引資料給家庭可支配所得表使用
c.to_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/birthnmarrige2017.csv')
# 新北各區出生婚姻概況並存成資料表

#---------------------------------------------------------------------------------
# 家庭可支配所得
import pandas as pd
district=pd.Series(['板橋區','中和區、永和區', '樹林區、鶯歌區、三峽區、土城區','三重區、蘆洲區',
                    '新莊區','汐止區','新店區', '五股區、泰山區、林口區、八里區', 
                    '淡水區、三芝區、石門區、金山區、萬里區',
                    '瑞芳區、深坑區、石碇區、坪林區、平溪區、雙溪區、貢寮區、烏來區'])
disposableincome=pd.Series(['223,490,091', '265,485,541', '231,750,561',
                           '221,977,685', '169,250,636','88,581,480','145,099,021',
                           '123,946,115','107,551,366', '28,239,363'])
dc=disposableincome.replace(to_replace=",", value="",regex=True)
familycount=pd.Series(['207,398', '255,471', '224,914', '221,122', '151,953', 
                       '86,440', '125,826', '114,998', '101,796', '44,010'])
fcount=familycount.replace(to_replace=",", value="",regex=True)
income=pd.concat([district,dc,fcount],axis=1)
income['dincome']=income[1].astype('float64')
income['fcount']=income[2].astype('float64') # 改變資料型態來計算
income['incomeperf']=(income['dincome']/income['fcount'])*1000
incomef=income.drop(columns=[1,2,'dincome','fcount'])
d29in=pd.DataFrame(d29)

for i in range(incomef.shape[0]):
    a = incomef.iloc[i,0].split("、",7)
    print(a)
    for d in range(d29in.shape[0]):
        if d29in.iloc[d,0] in a:
            d29in.loc[d,'dincomeperf']=incomef.iloc[i,1]
d29in.to_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/incomearea106.csv')
# 新北各區家庭可支配所得並存成資料表
#---------------------------------------------------------------------------------

# 學歷
import json
import pandas as pd
with open(r'/Users/emilykuo/Desktop/python專題/原始資料/106學歷.json') as file:
    edu=json.load(file)
    edu=edu["responseData"]

pd_edu = pd.DataFrame(edu)

pd_edu ['county']=pd_edu["site_id"].apply(lambda x: x[0:3]) 
pd_edu["site_id"]=pd_edu["site_id"].apply(lambda x: x[3:6]) 
NTmask=pd_edu['county']=='新北市'
pd_edu=pd_edu[NTmask]

pd_edur=pd_edu.iloc[:,4:51].astype('float64')
pd_edur["site_id"]=pd_edu.loc[:,'site_id']
      
pd_edur['6']=pd_edur.iloc[:,1:5].sum(axis=1)    #受過博士等級教育（含肄業與畢業）＃人數    
pd_edur['5']=pd_edur.iloc[:,5:9].sum(axis=1)    #受過碩士等級教育（含肄業與畢業）＃人數
pd_edur['4']=pd_edur.iloc[:,9:21].sum(axis=1)   #受過大學等級教育（含肄業與畢業）＃人數
pd_edur['3']=pd_edur.iloc[:,21:31].sum(axis=1)  #受過高中等級教育（含肄業與畢業）＃人數
pd_edur['2']=pd_edur.iloc[:,31:39].sum(axis=1)  #受過國中等級教育（含肄業與畢業）＃人數
pd_edur['1']=pd_edur.iloc[:,39:47].sum(axis=1)  #小學等級教育（含肄業與畢業與未受教育）＃人數

edulevels=pd_edur.drop(pd_edur.columns[1:47],axis=1)
edulevels=edulevels.groupby("site_id").sum()

edulevels['eduscore']=(edulevels['6']*6+edulevels['5']*5+edulevels['4']*4
                       +edulevels['3']*3\
                       +edulevels['2']+edulevels['1'])/edulevels['edu_age_15up_total']
edulevelsarea=edulevels.drop(edulevels.columns[0:7],axis=1)

edulevelsarea.to_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/edulevels.csv')
# 新北各區學歷等級指標並存成資料表
#---------------------------------------------------------------------------------


# 犯罪比數
import pandas as pd
crime=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/犯罪資料_000.csv')
print(crime)
mskcr106=crime['date'].between(1060000,1061231, inclusive=False) #篩選106年資料
crime106=crime[mskcr106]
crmloc=crime106.groupby("location")
crmtye=crime106.groupby("type")
print(crmtye.size()) #確認犯罪類型

crmhouse=crmtye.get_group("住宅竊盜")
crmhouseloc=crmhouse.groupby("location").count()
crmtype106=crmhouseloc.rename({"type":"crmhouse"},axis='columns')
crmtype106f=crmtype106.drop(columns="date")

crmcar=crmtye.get_group("汽車竊盜")
crmcarloc=crmcar.groupby("location").count()
crmcarloc=crmcarloc.rename({"type":"crmcar"},axis='columns')
crmtype106f1=crmcarloc.drop(columns="date")

crmbyc=crmtye.get_group("自行車竊盜")
crmbycloc=crmbyc.groupby("location").count()
crmbycloc=crmbycloc.rename({"type":"crmbyc"},axis='columns')
crmtype106f2=crmbycloc.drop(columns="date")
#機車竊盜有許多筆不分區資料故不納入

# 合併犯罪資料
crm106= crmtype106f.merge(crmtype106f1, left_on=('location'), right_on=('location'),
                          how='outer')
crm106= crm106.merge(crmtype106f2, left_on=('location'), right_on=('location'),
                     how='outer')
crm106.reset_index(drop=False, inplace=True)
crm106['Area']=crm106['location'].apply(lambda x: x[3:6])
crm106.to_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/crm106.csv')
# 整理新北各區竊盜情況概況

# 婦幼犯罪地點資料
import pandas as pd
wkcrm=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/易發生婦幼被害犯罪地點資料(+增加年度資料)_000.csv')
wkcrm106msk= wkcrm["year"]=="106年"
wkcrm106=wkcrm[wkcrm106msk]
wkcrm106['location'].apply(lambda x: x[3:6])
wkcrm106['Area']=wkcrm106['location'].apply(lambda x: x[3:6])
wkcrm106f=wkcrm106.groupby("Area").count()
wkcrmff=wkcrm106f.drop(columns=["year","six_months","police","precinct"])
crm106f= crm106.merge(wkcrmff, left_on=('Area'), right_on=('Area'), how='outer')
crm106f.to_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/crm106f.csv')
# 新北各區竊盜情況概況合併婦幼犯罪地點資料


# 合併區域人口資料算出犯罪萬分率
crimerate=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/crm106f.csv',index_col=0)
pplframe=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/pplframe.csv',index_col=0)
crimerate=crimerate.merge(pplframe, left_on=('Area'), right_on=('Area1'),how='outer')
crimerate['crmhouse']=(crimerate['crmhouse']/crimerate['ppl'])*10000
crimerate['crmcar']=(crimerate['crmcar']/crimerate['ppl'])*10000
crimerate['crmbyc']=(crimerate['crmbyc']/crimerate['ppl'])*10000
crimerate['location_y']=(crimerate['location_y']/crimerate['ppl'])*100000

crimerate=crimerate.drop(crimerate.columns[4],axis=1)
crimerate=crimerate.drop(crimerate.columns[6:11],axis=1)
crimerate['location_x']=crimerate['Area1']
crimerate=crimerate.drop(crimerate.columns[5],axis=1)
crimerate.to_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/crm106rate.csv')
# 新北各區竊盜與婦幼犯罪的萬分率
#---------------------------------------------------------------------------------

# 車禍統計
import pandas as pd
a1=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/trafficA1.csv')
a2=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/trafficA2.csv')
a1['year']=a1['yearmonth'].apply(lambda x: x[0:3]) #新增一欄只有年份的資料

a1106mask=a1['year']=="106"
a1106=a1[a1106mask]#篩選106年資料
print(a1106.info())
a1106['field8-1']=a1106['field8'].astype('float64') # 資料欄位為物件,將其轉為浮點
a1106f=a1106.drop(columns=['field8','year','yearmonth'])
a1106f['sum']=a1106f.iloc[:,3:12].sum(axis=1) #累積死傷人數總和
a1106ff=a1106f.drop(['field1','field2','field3','field4','field5','field6',
                     'field7','field9','field8-1'],axis=1)

a1106ftye=a1106ff.groupby("people")
a1106die=a1106ftye.get_group("死亡人數")
a1106diearea=a1106die.groupby("district").sum()
a1106dieareaf=a1106diearea.rename({"sum":"dieppl"},axis='columns')

a1106hurt=a1106ftye.get_group("受傷人數")
a1106hurtarea=a1106hurt.groupby("district").sum()
a1106hurtareaf=a1106hurtarea.rename({"sum":"hurtppl"},axis='columns')
a1106com=a1106dieareaf.merge(a1106hurtareaf,left_on=('district'), 
                             right_on=('district'), how='outer')

import pandas as pd
a2=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/trafficA2.csv')
a2=a2.replace(to_replace=["交叉路口：","一般地址：","其他：","省道：",
                          "新北市","鄉道：","市/縣","道："], value="",regex=True)
#處理地址格式方便抓取區域欄位
a2['Area']=a2['location'].apply(lambda x: x[0:3]) 
a2area=a2.groupby("Area").sum()
a2area=a2area.rename({"field1":"a2hurtppl"},axis='columns')

a1106com.reset_index(drop=False, inplace=True) 
a1a2com=a1106com.merge(a2area,left_on='district', right_on='Area', how='outer')
a1a2com.to_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/ca106.csv')

# 新北各區車禍概況
# 合併區域人口資料算出車禍萬分率
caraccident=pd.read_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/ca106.csv',index_col=0)
carate=caraccident.merge(pplframe, left_on=('district'), right_on=('Area1'),how='outer')
carate['dieppl']=(carate['dieppl']/carate['ppl'])*10000
carate['hurtppl']=(carate['hurtppl']/carate['ppl'])*10000
carate['a2hurtppl']=(carate['a2hurtppl']/carate['ppl'])*10000

carate=carate.drop(carate.columns[4:10],axis=1)
carate.to_csv(r'/Users/emilykuo/Desktop/python專題/原始資料/afterwash/carate.csv')
# 新北各區竊盜車禍萬分率


