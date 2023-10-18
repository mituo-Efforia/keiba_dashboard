import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import time
from tqdm import tqdm


#レースデータを取得する関数
def race_scrape(race_id_list):
    race_data={}
    for race_id in tqdm(race_id_list):
        time.sleep(1)
        try:
            url_id='https://db.netkeiba.com/race/' + race_id
            #スクレイピング
            res = requests.get(url_id) 
            html_content = res.content
            soup = BeautifulSoup(html_content,'html.parser')
            encoding = soup.original_encoding
            df = pd.read_html(html_content,encoding='EUC-JP')[0]
            #データフレームの整形
            df = df.rename(columns=lambda x: x.replace(' ',''))
            df['性別'] = df['性齢'].str[0]
            df['年齢'] = df['性齢'].str[1:3]
            #horse_idの抽出
            horse_a_list = soup.find("table",attrs={"summary" : "レース結果"}).find_all("a",attrs={"href":re.compile("^/horse")})
            horse_id_list=[]
            for h in horse_a_list:
                horse_id = re.findall(r"\d+",h["href"])
                horse_id_list.append(horse_id[0])
            #jockey_idの抽出
            jockey_a_list = soup.find("table",attrs={"summary" : "レース結果"}).find_all("a",attrs={"href":re.compile("^/jockey")})
            jockey_list = []
            for j in jockey_a_list:
                jockey_id = re.findall(r'\d+',j['href'])
                jockey_list.append(jockey_id[0])
            #trainer_idの抽出
            trainer_a_list = soup.find("table",attrs={"summary" : "レース結果"}).find_all("a",attrs={"href":re.compile("^/trainer")})
            trainer_list = []
            for j in trainer_a_list:
                trainer_id = re.findall(r'\d+',j['href'])
                trainer_list.append(trainer_id[0])
            df['horse_id'] = horse_id_list
            df['jockey_id'] = jockey_list
            df['trainer_id'] = trainer_list
            #indexをrace_idにする。
            df.index=[race_id]*len(df)
            race_data[race_id] = df
        #存在しないrace_idを読み込んでエラーを出した場合そのまま継続するようにする。(IndexError,AttributeErrorのケースがある)
        except IndexError:
                continue
        except AttributeError:
                continue
        #wifiの接続が切れた時などでも途中までのデータを返せるようにする
        except Exception as e:
            print(e)
            break
            #Jupyterで停止ボタンを押した時の対処
        except:
            break
    #pd.DataFrame型にして一つのデータにまとめる。
    race_data_df = pd.concat([race_data[key] for key in race_data])
        
    return race_data_df



#馬のデータを取得する関数
def horse_resluts(horse_id_list):
    horse_data ={}
    for horse_id in tqdm(horse_id_list):
        time.sleep(1)
        try:
            url = 'https://db.netkeiba.com/horse/' + str(horse_id)
            res = requests.get(url)
            html_content = res.content
            soup = BeautifulSoup(html_content,'html.parser')
            df = pd.read_html(url,encoding='EUC-JP')[3]

            #受賞歴があると3番目の配列に受賞歴のdataframeが入ってしまうため
            if df.columns[0] =='受賞歴':
                df=pd.read_html(url,encoding='EUC-JP')[4]
            df.index = [horse_id] * len(df)
            horse_data[horse_id] = df
            race_a_list=soup.find("table",attrs={"class":"db_h_race_results nk_tb_common"}).\
                         find_all("a",attrs={"href":re.compile("^/race")})
            race_id_list =[]
            for h in race_a_list:
                race_id = re.findall(r"[A-Za-z0-9]{12}",h['href'])
                race_id_list.append(race_id)
            race_id_list
            #race_id_listがこのままだと入れ子状態になっているため、直す。
            race_id_list_r = [item for sublist in race_id_list for item in sublist]
            #リスト内の重複を削除。setだと順番が変わってしまうのでdict.formkeys()を使う
            race_id_list=list(dict.fromkeys(race_id_list_r))
            df['race_id'] = race_id_list
        except IndexError :
            continue
        except AttributeError :
            continue
        except UnicodeDecodeError :
             continue
        except Exception as e:
            print(e)
            break
        except :
            break
    
    #print(horse_data)
    #DataFrame型にして一つにまとめる
    horse_data_df  = pd.concat([horse_data[key] for key in horse_data])

    return horse_data_df