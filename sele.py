import time                            # スリープを使うために必要
from selenium import webdriver         # Webブラウザを自動操作する（python -m pip install selenium)
import chromedriver_binary             # パスを通すためのコード
from selenium.webdriver.chrome.options import Options # オプションを使うためのコード
import pandas as pd
import datetime
import os
import csv



#マイビジネス地図ページまでスクレイピングしてページ数と何番目かを出力
#店舗名とキーワードを引数にする
def selen(shop_name,keyw):
    count = True
    page = 1
    
    option = Options()                          # オプションを用意
    option.add_argument('--incognito')  # シークレットモード

    driver = webdriver.Chrome(options=option)            # Chromeを準備
    
    driver.get('https://www.google.com/')       # Googleを開く
    search = driver.find_element_by_name('q')   # HTML内で検索ボックス(name='q')を指定する
    search.send_keys(keyw)             # 検索ワードを送信する
    search.submit()                             # 検索を実行
    
    time.sleep(5)
    
#    マップページに進む
    url = driver.find_element_by_class_name("DLOTif")
    url.click()
    
    time.sleep(5)
    
    
    try:
         #店舗名が出てくるまで繰り返す
        while count:
    #        表示ページの店舗をすべて取得
            shop = shop_list(driver)
            if shop_name in shop:
                for o in range(len(shop)):
                    if shop[o] == shop_name:
                        result = f"{page}ページ " + f"{o+1}番目"
                        count = False
                break
            #ない場合
            else:
                element = driver.find_element_by_link_text("次へ")
                link = element.get_attribute("href")
                #画像のリンクをクリック
                element.click()

                page += 1       #ページ数をカウント

        #        操作するURLをリンク先に変更
                driver.get(link)
                urls = link
                
    except:
        result = "なし"
 
    driver.quit()
    return result

    
    

#ページ中のショップ名取得
def shop_list(dri):
    #ショップ名を取得
    shops = dri.find_elements_by_class_name("dbg0pd")
    shop = []

    #全てテキストに変換して配列に入れなおす
    for i in shops:
        shop.append(i.text)
    return shop



#csvから店舗名とキーワードを取得してスクレイピング
def shop_keys():
    df = pd.read_csv('shops.csv', encoding="cp932")
#    1行ずつデータを取得する
    rd = df.iterrows()
#    ある分だけ繰り返す
    for i,v in rd:
        name = v["店舗名"]
        keywd1 = v["キーワード１"]
        keywd2 = v["キーワード２"]
        keywd3 = v["キーワード３"]
        
        keywds = [keywd1,keywd2,keywd3]
        
#        キーワード検索の結果をまとめるための変数
        ranks = []

    
#        スクレイピングする
        for n in keywds:
            rank = selen(name,n)
            ranks.append(rank)
        
#        本日の日付を取得
        today = datetime.datetime.today().strftime("%Y/%m/%d")#フォーマットの指定
#        保存するファイル名
        memory_file = name + ".csv"    
#        ファイル存在確認     
        file_check = os.path.isfile(memory_file)
    
#    ファイルが存在すれば上書き、なければ新規作成
        if file_check:
            list_csv = [today,ranks[0],ranks[1],ranks[2]]
            with open(memory_file, "a", encoding="utf_8_sig") as f:
                writer = csv.writer(f)
                writer.writerow(list_csv)
        else:
            list_df = pd.DataFrame([today,ranks[0],ranks[1],ranks[2]])
            list_df.index = ["日付","キーワード１","キーワード２","キーワード３"]

    #        indexとcolumnを入れ替えて追記で出力
    #        indexの0を消すためにはここにindex=Falseを入れる
            list_df.T.to_csv(memory_file, mode='a',encoding="utf_8_sig",index=False)

#        ranksを空に戻す
        ranks = []

    

def test():
    today = datetime.datetime.today().strftime("%Y/%m/%d")#フォーマットの指定
    ranks = ["あいうえお","かきくけこ","さしすせそ"]
    memory_file = "・ＭＰＭ・.csv"
    file_check = os.path.isfile(memory_file)
    if file_check:
        list_csv = [today,ranks[0],ranks[1],ranks[2]]
        with open(memory_file, "a", encoding="utf_8_sig") as f:
            writer = csv.writer(f)
            writer.writerow(list_csv)
    else:
        list_df = pd.DataFrame([today,ranks[0],ranks[1],ranks[2]])
        list_df.index = ["日付","キーワード１","キーワード２","キーワード３"]

#        indexとcolumnを入れ替えて追記で出力
#        indexの0を消すためにはここにindex=Falseを入れる
        list_df.T.to_csv(memory_file, mode='w',encoding="utf_8_sig",index=False)
    

    
if __name__ == "__main__":
    test()
    

    
