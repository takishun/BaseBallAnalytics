#!/usr/bin/env python
# coding: utf-8

# In[65]:


import pandas as pd
import ssl
import matplotlib
import os
from matplotlib import pyplot as plt, font_manager

get_ipython().run_line_magic('matplotlib', 'inline')
ssl._create_default_https_context = ssl._create_unverified_context

#####################################################################
###フォント設定用コード##############################################
font_manager._rebuild()
if os.name=='nt':
    #windows用
    font_dir=font_manager.win32FontDirectory()
else:
    #mac用
    font_dir='/Users/pydata/Library/Fonts/'
font_path=os.path.join(font_dir,'SourceHanCodeJP-Regular.otf')
font=font_manager.FontProperties(fname=font_path,size=14)
#####################################################################

def TeamTotalData(url_list):
    """
    チーム勝敗表と打撃、守備、投手成績をスクレイピングして一つのテーブル統合
    """

def scraping_data_Top_batter(url):
    """
    各リーグのバッタートップ30のデータをスクレイピングする。
    http://npb.jp/bis/2019/stats/bat_c.html　セ・リーグ
    http://npb.jp/bis/2019/stats/bat_p.html　パ・リーグ
    １．データクローリング
    ２．データ加工
    ３．コラム名修正
    ４．不要な行の削除
    ５．データを返す
    """
    data = pd.read_html(url)
    data[0]
    bat_c = data[0]
    bat_c = bat_c.drop(0)
    bat_c.head()
    bat_c.columns = ['順　位', '選　手', 'チーム', '打　率', '試　合', '打　席', '打　数', '得　点', '安　打', '二塁打',
       '三塁打', '本塁打', '塁　打', '打　点', '盗　塁', '盗塁刺', '犠　打', '犠　飛', '四　球', '故意四',
       '死　球', '三　振', '併殺打', '長打率', '出塁率']
    bat_c.head()
    bat_c = bat_c.drop(1)
    bat_c = bat_c.reset_index(drop=True)
    bat_c[['順　位', '打　率', '試　合', '打　席', '打　数', '得　点', '安　打', '二塁打',
       '三塁打', '本塁打', '塁　打', '打　点', '盗　塁', '盗塁刺', '犠　打', '犠　飛', '四　球', '故意四',
       '死　球', '三　振', '併殺打', '長打率', '出塁率']] = bat_c[['順　位', '打　率', '試　合', '打　席', '打　数', '得　点', '安　打', '二塁打',
       '三塁打', '本塁打', '塁　打', '打　点', '盗　塁', '盗塁刺', '犠　打', '犠　飛', '四　球', '故意四',
       '死　球', '三　振', '併殺打', '長打率', '出塁率']].astype(float)
    
    return bat_c

def scrapoing_data_Top_pitcher(url):
    """
    プロ野球のリーグトップの投手のデータをスクレイピングする
    """
    
def scraping_data_Team_batter(url):
    """
    各チームのバッターのデータを収集する
    """
    a = pd.read_html(url)
    b = a[0]
    b = b.drop(0)
    b.columns = b.loc[1]
    b = b.drop(1)
    b = b.reset_index(drop=True)
    b[['打　率', '試　合', '打　席', '打　数', '得　点', '安　打', '二塁打',
           '三塁打', '本塁打', '塁　打', '打　点', '盗　塁', '盗塁刺', '犠　打', '犠　飛', '四　球', '故意四',
           '死　球', '三　振', '併殺打', '長打率', '出塁率']] = b[['打　率', '試　合', '打　席', '打　数', '得　点', '安　打', '二塁打',
           '三塁打', '本塁打', '塁　打', '打　点', '盗　塁', '盗塁刺', '犠　打', '犠　飛', '四　球', '故意四',
           '死　球', '三　振', '併殺打', '長打率', '出塁率']].astype(float)
    return b

def scraping_data_Team_pitcher(url):
    """
    各チームのピッチャーのデータを収集する
    """
    data = pd.read_html(url)
    data = data[0]
    data = data[:-1]
    data = data.replace('-','0')
    
    data[['防御率', '登板', '先発', '完投', '完封', 'QS', '勝利', '敗戦',
         'ホ|ルド','HP', 'セ|ブ', '勝率', '投球回', '被安打', '被本塁打', '奪三振', '奪三振率', '与四球',
        '与死球','暴投', 'ボ|ク', '失点', '自責点', '被打率', 'K/BB', 'WHIP']] = data[['防御率', '登板', '先発', '完投', '完封', 'QS', '勝利', '敗戦',
         'ホ|ルド','HP', 'セ|ブ', '勝率', '投球回', '被安打', '被本塁打', '奪三振', '奪三振率', '与四球',
        '与死球','暴投', 'ボ|ク', '失点', '自責点', '被打率', 'K/BB', 'WHIP']].astype(float)
    
    return data

def CyberMetricsBatter(df):
    """
    バッターのセイバーメトリックス指標を計算して、データ加工する
    OPS:得点力
    IsoP:パワー指標
    IsoD:選球眼
    BB/K:選球眼
    BIBIP:運の要素を取り出す指標
    A:出塁能力
    B:進塁能力
    C:出塁機会
    RC:得点力
    RC27:この選手が9人いたとして、1試合の得点能力に換算した式
    AB/HR:1本塁打打つまでにかかる打数
    PA/K:三振するまでにかかる打数
    PS:機動力とパワーを兼ね添えてるかを見る
    """
    try:
        df['OPS'] = df['長打率']+df['出塁率']  #得点力
    except KeyError:
        print('KeyError')
    try:
        df['IsoP'] = df['長打率']-df['打率'] #パワー
    except KeyError:
        print('KeyError')
    try:
        df['IsoD'] = df['出塁率']-df['打率'] #選球眼
    except KeyError:
        print('KeyError')
    try:
        df['BB/K'] = df['四球']/df['三振'] #選球眼
    except KeyError:
        print('KeyError')    
    try:
        df['BABIP'] = (df['安打']-df['本塁打'])/(df['打数']-df['三振']-df['本塁打']+df['犠飛'])
    except KeyError:
        print('KeyError')
    try:
        A = df['安打']+df['四球']+df['死球']-df['盗塁死']-df['併殺打'] #出塁能力
        B = df['塁打']+0.26*(df['四球']+df['死球'])+0.53*(df['犠飛']+df['犠打'])+0.64*df['盗塁']-0.03*df['三振']#進塁能力
        C = df['打数']+df['四球']+df['死球']+df['犠飛']+df['犠打']#出塁機会
        df['RC']=(A+2.4*C)*(B+3*C)/(9*C)-0.9*C
        TO = df['打数']-df['安打']+df['犠打']+df['犠飛']+df['盗塁死']+df['併殺打']
        df['RC27'] = 27*df['RC']/TO #この選手が9人いたとして、1試合の得点能力に換算した式
    except KeyError:
        print('KeyError')
    try:
        df['AB/HR'] = df['打数']/df['本塁打']#1本塁打打つまでにかかる打数
    except KeyError:
        print('KeyError')
    try:
        df['PA/K'] = df['打数']/df['三振']#三振するまでにかかる打数
    except KeyError:
        print('KeyError')
    try:
        df['PS'] = (df['本塁打']+2*df['盗塁'])/(df['本塁打']+df['盗塁'])#機動力とパワーを兼ね添えてるかを見る     
    except KeyError:
        print('KeyError')
        
    except ZeroDivisionError:
        print('0除算がありました。')
    
    finally:
        print('計算終了')

    return df

def CyberMetricsPitcher(df):
    """
    ピッチャーのセイバーメトリックス指標を計算して、データ加工する
    FIP:野手による影響を受けない結果（被本塁打、三振、四死球など）のみで投手の能力を評価した指標
    QS%:先発登板数に対するQSの割合
    LOB:ランナーを出した状態で失点しなかった指標
    
    """
    
    try:
        df['FIP'] = (13*df['被本塁打']+(df['与四球']+df['与死球'])*3-df['奪三振']*2)/df['投球回']+3.12
    except KeyError:
        print('key error exception')
    try:
        df['LOB'] = (df['被安打']+df['与四球']+df['与死球']-df['失点'])/(df['被安打']+df['与四球']+df['与死球']-1.4*df['被本塁打'])
    except KeyError:
        print('key error exception')
    try:
        df['BB/9']= df['与四球']*9/df['投球回']
    except KeyError:
        print('key error exception')
    try:
        df['HR/9']= df['被本塁打']*9/df['投球回']
    except KeyError:
        print('key error exception')
    try:
        df['QS%'] = df['QS']/df['先発']    
    except KeyError:
        print('key error exception')
    try:
        #(与四球 + 被安打) ÷ 投球回
        df['WHIP']=(df['与四球']+df['被安打'])/df['投球回']
    except KeyError:
        print('key error exception')
    try:
        #(与四球 + 被安打) ÷ 投球回
        df['K/BB']=df['奪三振']/df['与四球']
    except KeyError:
        print('key error exception')
    try:
        # (安打 - 本塁打) ÷ (打数 - 奪三振 - 本塁打 + 犠飛)
        df['BABIP']=(df['被安打']-df['被本塁打'])/(df['打者']-df['奪三振']-df['被本塁打'])
    except KeyError:
        print('key error exception')  

    except ZeroDivisionError:
        print('0除算がありました。')
    
    
    finally:
        print('計算終了')
        
    return df



def To_csv(df,filename='output.csv',enc='utf-8'):
    df.to_csv(filename,encoding=enc)

if __name__ == "__main__":
    team_name = ['l','h','f','b','m','e','c','s','g','db','d','t']
    year = ['2019']
    for i in year:
        for j in team_name:
            data = scraping_data_Team_batter('http://npb.jp/bis/'+str(i)+ '/stats/idb1_'+str(j)+'.html')
            data = CyberMetricsBatter(data)
            data.to_csv('batter_data_'+str(i)+'_'+str(j),index=False)
# In[73]:


if __name__ == "__main__":
    url_list=['http://npb.jp/bis/2019/stats/bat_c.html','http://npb.jp/bis/2019/stats/bat_p.html']
    name_list=['central_batterTOP30','pacific_batterTOP30']
    num = 0
    for i in url_list:
        data = scraping_data_Top_batter(i)
        scd = CyberMetricsBatter(data)
        scd.to_csv(name_list[num]+'.csv',sep=',',index=False)
        num+=1


# In[70]:


if __name__ =="__main__":
    team_num = ['1','2','3','4','5','6','7','8','9','11','12','376']
    name_list=['G','Ys','BS','D','T','C','La','F','Lo','O','H','E']
    num = 0
    for i in team_num:
        url = 'https://baseball.yahoo.co.jp/npb/teams/'+str(i)+'/memberlist?type=p'
        data = scraping_data_Team_pitcher(url)
        cal_data = CyberMetricsPitcher(data)
        cal_data.to_csv('TeamPitcherData_'+name_list[num]+'.csv',sep=',',index=False)
        num+=1


# In[75]:


a = pd.read_csv('TeamPitcherData_D.csv')


# In[76]:


a.mean()


# In[ ]:




