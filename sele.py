import time                            # スリープを使うために必要
from selenium import webdriver         # Webブラウザを自動操作する（python -m pip install selenium)
import chromedriver_binary             # パスを通すためのコード
from selenium.webdriver.chrome.options import Options # オプションを使うためのコード

option = Options()                          # オプションを用意
option.add_argument('--incognito')  # シークレットモード

driver = webdriver.Chrome(options=option)            # Chromeを準備

#クロームを開く
def selen(url):
    driver.get(url)  # Googleを開く
    time.sleep(5)                          # 5秒間待機

#ショップ名取得関数
def shop_list():
    #ショップ名を取得
    shops = driver.find_elements_by_class_name("dbg0pd")
    shop = []

    #全てテキストに変換して配列に入れなおす
    for i in shops:
        shop.append(i.text)
    return shop



urls = "https://www.google.com/search?hl=ja&q=%E5%87%BA%E9%9B%B2%E3%80%80%E7%BE%8E%E5%AE%B9%E5%AE%A4&npsic=0&rflfq=1&rlha=0&rllag=35369436,132744442,1407&tbm=lcl&ved=2ahUKEwjv2ZCVwrDqAhUJVN4KHYzgDPMQjGp6BAgLED4&rldoc=1#rlfi=hd:;si:;mv:[[35.3840228,132.76427329999999],[35.3336536,132.7191841]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2"







page = 1
name = "・ＭＰＭ・"

count = True

#selen(urls)
# 


#店舗名が出てくるまで繰り返す
while count:
    #表示ページに存在するかの確認
    selen(urls)
    shop = shop_list()
    if name in shop:
        for o in range(len(shop)):
            if shop[o] == name:
                print(f"{page}ページ")
                print(f"{o+1}番目")
                count = False
        break
    #ない場合
    else:
        element = driver.find_element_by_link_text("次へ")
        link = element.get_attribute("href")
        #画像のリンクをクリック
        element.click()
        
        page += 1
        
#        操作するURLをリンク先に変更
        driver.get(link)
        urls = link
        

driver.quit()  
    