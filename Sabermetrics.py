#!/usr/bin/env python
# coding: utf-8

# In[23]:


import pandas as pd
import numpy as np

def SabermetricsBatter(df):
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
    Spd：走塁能力
    簡易RF：レンジファクター、守備寄与率
    """
    try:
        df['OPS'] = df['長打率']+df['出塁率']  #得点力
    except KeyError:
        print('KeyError: can not make OPS')
    try:
        df['IsoP'] = df['長打率']-df['打率'] #パワー
    except KeyError:
        print('KeyError: can not make IsoP')
    try:
        df['IsoD'] = df['出塁率']-df['打率'] #選球眼
    except KeyError:
        print('KeyError: can not make IsoD')
    try:
        df['BB/K'] = df['四球']/df['三振'] #選球眼
    except KeyError:
        print('KeyError: can not make BB/K')
    try:
        df['BABIP'] = (df['安打']-df['本塁打'])/(df['打数']-df['三振']-df['本塁打']+df['犠飛'])
    except KeyError:
        print('KeyError: can not make BABIP')
    try:
        A = df['安打']+df['四球']+df['死球']-df['盗塁刺']-df['併殺打'] #出塁能力
        B = df['塁打']+0.26*(df['四球']+df['死球'])+0.53*(df['犠飛']+df['犠打'])+0.64*df['盗塁']-0.03*df['三振']#進塁能力
        C = df['打数']+df['四球']+df['死球']+df['犠飛']+df['犠打']#出塁機会
        df['RC']=(A+2.4*C)*(B+3*C)/(9*C)-0.9*C
        TO = df['打数']-df['安打']+df['犠打']+df['犠飛']+df['盗塁刺']+df['併殺打']
        df['RC27'] = 27*df['RC']/TO #この選手が9人いたとして、1試合の得点能力に換算した式
    except KeyError:
        print('KeyError: can not make RC27')
    try:
        df['AB/HR'] = df['打数']/df['本塁打']#1本塁打打つまでにかかる打数
    except KeyError:
        print('KeyError: can not make AB/HR')
    try:
        df['PA/K'] = df['打数']/df['三振']#三振するまでにかかる打数
    except KeyError:
        print('KeyError: can not make PA/K')
    try:
        df['PS'] = (df['本塁打']*2*df['盗塁'])/(df['本塁打']+df['盗塁'])#機動力とパワーを兼ね添えてるかを見る     
    except KeyError:
        print('KeyError: can not make PS')
    
    try:
        steel_ratio=((df['盗塁']+3)/(df['盗塁']+df['盗塁刺']+7)-0.4)*20
        try_steel=np.sqrt((df['盗塁']+df['盗塁刺'])/(df['安打']+df['四球']+df['死球']))/0.07
        three_base_ratio=df['三塁打']/(df['打数']-df['本塁打']-df['三振'])/0.02*10
        run_ratio=((df['得点']-df['本塁打'])/(df['安打']+df['四球']+df['死球']-df['本塁打'])-0.1)/0.04
        df['Spd']=(steel_ratio+try_steel+three_base_ratio+run_ratio)/4.0
    except KeyError:
        print('KeyError: can not make Spd')
        
    try:
        df['簡易RF']=(df['刺殺']+df['補殺'])/df['試合']
    except KeyError:
        print('KeyError: can not make RF')
    
    except ZeroDivisionError:
        print('0除算がありました。')
    
    finally:
        print('計算終了')

    return df

def SabermetricsPitcher(df):
    """
    ピッチャーのセイバーメトリックス指標を計算して、データ加工する
    FIP:野手による影響を受けない結果（被本塁打、三振、四死球など）のみで投手の能力を評価した指標
    QS%:先発登板数に対するQSの割合
    LOB:ランナーを出した状態で失点しなかった指標
    
    """
    try:
        df['FIP'] = (13*df['本塁打']+(df['四球']+df['死球'])*3-df['三振']*2)/df['投球回']+3.12
    except KeyError:
        print('key error exception: can not make FIP')
    try:
        df['LOB'] = (df['安打']+df['四球']+df['死球']-df['失点'])/(df['安打']+df['四球']+df['死球']-1.4*df['本塁打'])
    except KeyError:
        print('key error exception: can not make LOB')
    try:
        df['BB/9']= df['四球']*9/df['投球回']
    except KeyError:
        print('key error exception: can not make BB/9')
    try:
        df['HR/9']= df['本塁打']*9/df['投球回']
    except KeyError:
        print('key error exception: can not make HR/9')
    try:
        df['QS%'] = df['QS']/df['先発']    
    except KeyError:
        print('key error exception: can not make QS%')
    try:
        #(与四球 + 被安打) ÷ 投球回
        df['WHIP']=(df['四球']+df['安打'])/df['投球回']
    except KeyError:
        print('key error exception: can not make WHIP')
    try:
        #(与四球 + 被安打) ÷ 投球回
        df['K/BB']=df['三振']/df['四球']
    except KeyError:
        print('key error exception: can not make K/BB')
    try:
        # (安打 - 本塁打) ÷ (打数 - 奪三振 - 本塁打 + 犠飛)
        df['BABIP']=(df['安打']-df['本塁打'])/(df['打者']-df['三振']-df['本塁打'])
    except KeyError:
        print('key error exception: can not make BABIP')

    except ZeroDivisionError:
        print('0除算がありました。')
    
    finally:
        print('計算終了')
        
    return df


# In[33]:


if __name__ == "__main__":
    data_pitch = pd.read_csv('Open_Pitch.csv')
    data_pitch = data_pitch[data_pitch['投球回']!='+']
    data_pitch = data_pitch.astype({'投球回':'float32'})
    data_hitter = pd.read_csv('Open_Hitter.csv')
    
    data_pitch = SabermetricsPitcher(data_pitch)
    data_hitter = SabermetricsBatter(data_hitter)
    
    data_pitch.to_csv('sabermetricsPitcher.csv',index=False)
    data_hitter.to_csv('sabermetricsHitter.csv',index=False)


# In[ ]:




