from selenium import webdriver
import time
import pandas as pd
import re
import datetime
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select


def janum_get():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")


    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝textからURLを受け取る処理＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

    class CreateUrl():
        
        def __init__(self):
            
            # テキストから取得したじゃらん番号入っている
            self.__yados_num = []
            
            # テキストから取得したURLが入っている
            self.__urls = []
            
        
        def url_create(self):
            
            with open('/Users/enokitoshiki/Desktop/ja_yado_num.txt', encoding='utf-8') as f:
                for row in f:
                    yado = row.rstrip()
                    self.__yados_num.append(yado)
                    
            for yado_num in self.__yados_num:
                global url
                url = ("https://www.jalan.net/yad" + str(yado_num) + "/")
                self.__urls.append(url)
                
                
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝textからURLを受け取る処理＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
                
        
                
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝CreateクラスにURLを送る処理＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

        def get_yado_num(self):
            
            for i in range(len(self.__urls)):
                # Createクラス（一件の宿情報を取得してくれるもの）にURLを引数に渡す
                get = Create(self.__urls[0])
                get_func = get.create_num()
                self.__urls.pop(0)
                driver.quit()
            
            
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝CreateクラスにURLを送る処理＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

        
            
    class Create(CreateUrl):
        
        
        def __init__(self,url):
            
            #CreateクラスでGetYadoクラスを作った時に引数で受け取ったULRがここで引き継がれる
            self.url = url
            self.link = []
            
            
        def access(self):
            
            global driver
            driver=webdriver.Chrome("/Users/enokitoshiki/anaconda3/envs/testskyper/selenium/chromedriver", chrome_options=chrome_options)
            driver.maximize_window()
            print(self.url)
            driver.get(self.url)
            
            
        #1ページの宿のscrapingを行う。   
        def yado_num_scraping(self):
            
            print(driver.current_url)
            current_url =  driver.current_url
            response = requests.get(current_url)
            response.encoding = response.apparent_encoding

            bs = BeautifulSoup(response.text, "html.parser")

            #宿の一覧を表示させる
            ol_tag = bs.find('ol')

            link = []
            
            #olタグの中から、aタグだけ抜き出す
            for a_tag in ol_tag.find_all("a"):
                link_url = a_tag["href"]

                #/yadoから始まるものだけ取り出す
                if re.match("/yad.*", link_url):

                    # yad332440みたいな形にする
                    link_url = link_url.split('/')[1]

                    #332440のみにする
                    link_url = link_url.split('yad')[1]
                    link.append(link_url)
                else:
                    pass

            #setを使うことで、リストの中の重複したものを無くし、辞書型で出力する
            yado_num = set(link)
            
            #set関数で出力された辞書型に0というvaluesを付け加える。
            yado_num = dict.fromkeys(yado_num, 0)

            #0を付け加えることで、keysを取り出すことできる　そうすることによって、宿番号をリスト型で表示してくれる
            yado_num = list(yado_num.keys())
            
            self.link.extend(yado_num)
            
            #次のページ分のリンクも入れないとだからクリアする
            link.clear()

        def repeat_next_page(self):
            
            global area
            area = driver.find_element_by_xpath('//*[@id="pankuzu"]/a[3]').text
            #エリアに移動する
            driver.find_element_by_xpath('//*[@id="pankuzu"]/a[3]').click()
            
            #エリアにある宿の数をとってくる
            area_yado_num = driver.find_element_by_xpath('//*[@id="search-tab"]/table[2]/tbody/tr[1]/td[1]/span[1]').text
            area_yado_num =float(area_yado_num)

            global click_num
            click_num = area_yado_num // 30.01
            print(click_num)


        def create_num(self):
            
            self.access()
            #何回クリックするかを調べる
            
            self.repeat_next_page()
            
            #1ページの宿のscrapingを行う
            self.yado_num_scraping()

            for click in range(int(click_num)):
                
                try:
                    driver.find_element_by_partial_link_text("次へ").click()
                except:
                    driver.find_element_by_class_name('karte-close').click()
                    
                    print("popアップ削除")
                    driver.find_element_by_partial_link_text("次へ").click()            
                #1ページの宿のscrapingを行う
                self.yado_num_scraping()
                time.sleep(1)
                
            print(self.link)
            print(len(self.link))           
            self.preservation()
                
                
        def preservation(self):
            with open("JA_number.txt" +  "：" + area , 'w', encoding='utf-8') as f:
                for get_num in self.link:
                    f.write(str(get_num) + "\n")
                    
                
    aa = CreateUrl()
    aa.url_create()
    aa.get_yado_num()
        
        
        
    # c = Create()
    # c.create_num()


    # repeat_next_page()
    print("完了")
    
if __name__ == '__main__':
    janum_get()