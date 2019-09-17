from selenium import webdriver
import time
import pandas as pd
import re
import datetime
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from .models import reviews, Yado


# driver.getはdriver=webdriver.Chrome()を使ったあとでないと起動しない
# driver=webdriver.Chrome("/Users/enokitoshiki/anaconda3/envs/testskyper/selenium/chromedriver")
# driver.maximize_window()

def jaget():
    print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")


    key_list = ["宿名","じゃらん番号",'エリア', '掲載順位','日付', '口コミ件数', "総合評価",'部屋', '風呂',
            '料理（朝食）', '料理（夕食）', '接客・サービス', '清潔感', '2食付き最安値', '素泊まり最安値','プラン数']


    ja_dic_list = {}
    for key in key_list:
        jayado_dc = dict.fromkeys([key], '')

        ja_dic_list.update(jayado_dc)
        

    with open(str(datetime.date.today())+ "JA.csv", 'w', encoding='utf-8') as f:
        for key in key_list:
            f.write(str(key) + ",")
        f.write('\n')
        


    class Create():
        
        def __init__(self):

            # テキストから取得したじゃらん番号入っている
            self.__yados_num = []
            
            # テキストから取得したURLが入っている
            self.__urls = []
        
        def url_create(self):
            
            #このファイルにじゃらんの番号を入れることによって、宿の口コミを取得できる。
            with open('./ys/ja_yado_num.txt', encoding='utf-8') as f:
                for row in f:
                    yado = row.rstrip()
                    self.__yados_num.append(yado)
                    
            for yado_num in self.__yados_num:
                global url
                url = ("https://www.jalan.net/yad" + str(yado_num) + "/")
                self.__urls.append(url)
                

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝ブラウザのキャッシュを消すための処理＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
                
        # この関数で、何回目でブラウザーを閉じて、口コミを取得するか決めている
        def get_yado_info(self):
            
            # 何回でdriver_quitをするか
            get_info_num = 2
            
            #set_repeat_num例) 5宿の情報を2何回に分けて情報を取得するか
            set_repeat_num = len(self.__urls) // get_info_num
            remaining = len(self.__urls) % get_info_num
            
            repeat_time = 0
            
            #repea回数は、全体の宿数/driver_quitするまでの宿数の数で表せれる
            while repeat_time < set_repeat_num:
                
                
                #driver_quitするまで行うfor文
                for i, num in enumerate(range(get_info_num)):
                    
                    #driver=webdriver.Chromeを最初に起動させるためにif文を書く
                    if i == 0:
                        
                        # driver.getはdriver=webdriver.Chrome()を使ったあとでないと起動しない
                        global driver
                        driver=webdriver.Chrome("./selenium/chromedriver", chrome_options=chrome_options)
                        driver.maximize_window()
                        
                    # GetYadoクラス（一件の宿情報を取得してくれるもの）にURLを引数に渡す
                        get = GetYado(self.__urls[0], self.__yados_num[0])
                        get_func = get.access_get()
                        self.__urls.pop(0)
                        self.__yados_num.pop(0)
                    else:
                        # GetYadoクラス（一件の宿情報を取得してくれるもの）にURLを引数に渡す
                        get = GetYado(self.__urls[0], self.__yados_num[0])
                        get_func = get.access_get()
                        self.__urls.pop(0)
                        self.__yados_num.pop(0)
                driver.quit()
                
                # 宿情報を取得した処理1セットが終わったら、カウント+1
                repeat_time += 1
            
            #remaining例) 5宿の情報を2何回に分けて情報を取得したら、残り一つの宿があまるからここで取得する。
            for i in range(remaining):
                
                driver=webdriver.Chrome("./selenium/chromedriver", chrome_options=chrome_options)
                driver.maximize_window()

                get = GetYado(self.__urls[0], self.__yados_num[0])
                get_func = get.access_get()

                self.__urls.pop(0)
                self.__yados_num.pop(0)
            driver.quit()
            
            

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝ブラウザのキャッシュを消すための処理＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

            
            

    class GetYado(Create):
        
        def __init__(self, url, ja_num):
            #CreateクラスでGetYadoクラスを作った時に引数で受け取ったULRがここで引き継がれる
            self.url = url
            self.ja_num = ja_num
            
            
            #上のkey_listを辞書にしたもの　ここに値を入れ込むようにしていく。
            self.__ja_reviews_dic = ja_dic_list        
        
            # 口コミの詳細ページで取得したものを入れておくリスト　例）料金、風呂の点数等
            self.__reviews_list = []
            
            
            self.__yado_list_all_page = []
            self.__yado_rank = []
            
            #宿のページ数がここに入れる
            self.__page_list = []
            
            #  yado_list1は、取得したh2タグから、宿泊施設|.*観光情報|.*その他宿情報|絞り込みを排除させたもの
            self.__yado_list1 = []
            
            
            
            
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝処理の順番＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    
        def access_get(self):
            driver.get(self.url)
            if driver.title == "エラー画面－じゃらんnet" or driver.title == "エラー画面":
                return
            self.__ja_reviews_dic["じゃらん番号"] = self.ja_num
            
            #口コミの処理を行う関数を呼び出す
            self.review_check()
            
            #プランの処理を行う関数を呼び出す
            self.plan_check()
            
            self.movement_area()
            self.repeat_next_page()
            self.yado_rank()
            
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝処理の順番＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝



            

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝口コミ処理＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
            
        def review_check(self):
            
            try:
                driver.find_element_by_partial_link_text("クチコミ").click()
                reviews_table = driver.find_element_by_xpath('//*[@id="contentsBody"]/div[2]/div').text 
            except:
                pass
            
            self.__ja_reviews_dic["宿名"] = driver.find_element_by_xpath('//*[@id="yado_header_hotel_name"]/a').text
            self.__ja_reviews_dic["エリア"] = driver.find_element_by_xpath('//*[@id="pankuzu"]/a[3]').text
            reviews = re.split('[\n："件"]',reviews_table)


    # reviewsの中の必要ないものをここではき出す
            for review in reviews:
                if review == "クチコミ総合" or review == "（「普通＝3.0」が評価時の基準です）" or review == "部屋" \
                    or review == "風呂" or review == "料理（朝食）" or review == "料理（夕食）" \
                    or review == "接客・サービス" or review == "清潔感" or review == "項目別の評価" \
                    or review == "サービス" or review == "立地" or review == "部屋" or review == "設備・アメニティ" \
                    or review == "風呂" or review == "食事" or review == "数" or review == '':
                    pass
                elif review == '－－－－－':
                    replace_review = review.replace('－－－－－', '')
                    self.__reviews_list.append(replace_review)
                elif review == '- ':
                    replace_review = review.replace('- ', '0')
                    self.__reviews_list.append(replace_review)
                else:
                    self.__reviews_list.append(review)
                    
            print(self.__reviews_list)
                    
            try:
                if "－ 有効クチコミ数に達していないためクチコミ評価は表示しておりません  "  == self.__reviews_list[0]:
                    
                    self.__ja_reviews_dic["総合評価"] = "0"
                    self.__ja_reviews_dic["部屋"] = "0"
                    self.__ja_reviews_dic["風呂"] = "0"
                    self.__ja_reviews_dic["料理（朝食）"] = "0"
                    self.__ja_reviews_dic["料理（夕食）"] = "0"
                    self.__ja_reviews_dic["接客・サービス"] = "0"
                    self.__ja_reviews_dic["清潔感"] = "0"
                    self.__ja_reviews_dic["日付"] = str(datetime.date.today())  
                    self.__ja_reviews_dic["口コミ件数"] = "0"              

                else:
                    self.__ja_reviews_dic["総合評価"] = self.__reviews_list[0]
                    self.__ja_reviews_dic["部屋"] = self.__reviews_list[1]
                    self.__ja_reviews_dic["風呂"] = self.__reviews_list[2]
                    self.__ja_reviews_dic["料理（朝食）"] = self.__reviews_list[3]
                    self.__ja_reviews_dic["料理（夕食）"] = self.__reviews_list[4]
                    self.__ja_reviews_dic["接客・サービス"] = self.__reviews_list[5]
                    self.__ja_reviews_dic["清潔感"] = self.__reviews_list[6]
                    self.__ja_reviews_dic["日付"] = str(datetime.date.today())
                    self.__ja_reviews_dic["口コミ件数"] = "0"
                
                    self.reviews_num_check()
                
            except:
                self.__reviews_list.clear()
                for review in range(7):
                    self.__reviews_list.append("0")
                    
                self.__ja_reviews_dic["総合評価"] = self.__reviews_list[0]
                self.__ja_reviews_dic["部屋"] = self.__reviews_list[1]
                self.__ja_reviews_dic["風呂"] = self.__reviews_list[2]
                self.__ja_reviews_dic["料理（朝食）"] = self.__reviews_list[3]
                self.__ja_reviews_dic["料理（夕食）"] = self.__reviews_list[4]
                self.__ja_reviews_dic["接客・サービス"] = self.__reviews_list[5]
                self.__ja_reviews_dic["清潔感"] = self.__reviews_list[6]
                self.__ja_reviews_dic["日付"] = str(datetime.date.today())
                self.__ja_reviews_dic["口コミ件数"] = "0"
                
            print("\n")        
            
        def reviews_num_check(self):
            
            reviews_nums = driver.find_element_by_xpath('//*[@id="contentsBody"]/div[3]/div[1]/dl/dd[1]').text
            reviews_num = re.split('[\n クチコミ 件]', reviews_nums)

            for review_num in reviews_num:
                if review_num == '':
                    pass
                else:
                    self.__ja_reviews_dic["口コミ件数"] = review_num

            if len(reviews_num) == 1:
                self.__ja_reviews_dic["口コミ件数"] = ""
            else:
                pass
                
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝口コミ処理＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
        
        

        
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝料金処理＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

        def plan_check(self):
            
            driver.find_element_by_link_text("料金・宿泊プラン").click()

            try:
                plan_table = driver.find_element_by_xpath('//*[@id="planlist-header"]/table[2]/tbody/tr/td/p/span').text
            except:
                plan_table = driver.find_element_by_xpath(' //*[@id="planlist-header"]/table/tbody/tr/td/p/span').text

            self.__ja_reviews_dic["プラン数"] = plan_table
            self.check_price()
            
            
        def check_price(self):
            print("check_price実行開始")
            
            driver.find_element_by_xpath("//select[@id='dyn_adult_num']/option[@value='2']").click()
            
            #2食付きの処理　※サイドバーで料金設定を行う場合があるのでtyr exceptを行う
            try:
                driver.find_element_by_xpath("//select[@id='dyn_meal_txt']/option[@value='3']").click()
                driver.find_element_by_xpath('//*[@id="research"]').click()
            except:
                driver.find_element_by_xpath('//*[@id="dyn_badget_tbl"]').click()
                time.sleep(1)
                
                #下にスクロールさせないとエラーが起きる。
                self.scroll_down()
                time.sleep(1)
                
                driver.find_element_by_xpath('//*[@id="jsi-mealType-block"]/ul/li[5]/label').click()
                driver.find_element_by_xpath('//*[@id="research"]').click()
            else:
                print("2食付きなし")
                
            #2食付きの最安値の処理を行ってくれる。
            #2食付きなしの場合で処理が回る場合があるので、ここでもtry, exceptを使う。
            try:
                dinner_breakfast = self.price_min()
                self.__ja_reviews_dic["2食付き最安値"] = dinner_breakfast
                print(dinner_breakfast)
                time.sleep(1)
            except:
                self.__ja_reviews_dic["2食付き最安値"] = "0"
                
            
            #素泊まりの処理　※サイドバーで料金設定を行う場合があるのでtyr exceptを行う
            try:
                driver.find_element_by_xpath("//select[@id='dyn_meal_txt']/option[@value='0']").click()
                driver.find_element_by_xpath('//*[@id="research"]').click()
            except:
                driver.find_element_by_xpath('//*[@id="dyn_badget_tbl"]').click()
                time.sleep(1)
                
                #下にスクロールさせないとエラーが起きる。
                self.scroll_down()
                time.sleep(1)
                
                driver.find_element_by_xpath('//*[@id="jsi-mealType-block"]/ul/li[2]/label').click()
                driver.find_element_by_xpath('//*[@id="research"]').click()
            else:
                print("素泊まりなし")
            
            #素泊まりの最安値の処理を行ってくれる。
            #素泊まりの場合で処理が回る場合があるので、ここでもtry, exceptを使う。
            try:
                stay_overnight = self.price_min()
                self.__ja_reviews_dic["素泊まり最安値"] = stay_overnight
                print(stay_overnight)
            except:
                self.__ja_reviews_dic["素泊まり最安値"] = "0"

        def price_min(self):
            
            #プランのをbeautifull soupで料金の一覧を取り出し、配列に料金を取り出す。
            #その中から、一番料金の安いものを取り出す。
            
            response = requests.get(driver.current_url)
            response.encoding = response.apparent_encoding

            bs = BeautifulSoup(response.text, "html.parser")
            div_plan_title_list =  bs.select("div.p-searchResults")

            price_list = []
            
            for price in div_plan_title_list[0].select("td.p-searchResultItem__perPersonCell"):
                price = price.text.strip().split("円")
                price = price[0]
                price = price.replace(",", "")
                price = int(price)
                price_list.append(price)
            return min(price_list)
        
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝料金処理＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    
    

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝エリア移動＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
        
        
        def movement_area(self):
            driver.find_element_by_link_text(self.__ja_reviews_dic["エリア"]).click()
            page_nums = driver.find_element_by_xpath('//*[@id="search-tab"]/table[2]/tbody/tr[1]/td[2]').text
            page_nums_split = re.split('[\n |]',page_nums)
            for page_num in page_nums_split:
                if page_num == "最初" or page_num == '' or  page_num ==  '前へ' \
                        or page_num == "次へ" or page_num == "最後" :
                    pass
                else:
                    page_int = int(page_num)
                    self.__page_list.append(page_int)

            

        def scrapping_get_h2(self):
            elements = driver.find_elements_by_tag_name('h2')
            for element in elements:
                yado_name = element.text
                if re.match('.*・宿泊施設|.*観光情報|.*その他宿情報|絞り込み',yado_name):
                    pass
                elif yado_name == '':
                    pass            
                else:
                    self.__yado_list1.append(yado_name)
                    
        def delete_advertisement(self):
            
            advertisement_num = len(self.__yado_list1) - 30
            
            global yado_list1
            yado_list1 = len(self.__yado_list1)
            
            if len(self.__yado_list1) > 30:
                while advertisement_num > 0:
                    self.__yado_list1.pop(0)
                    advertisement_num += -1
                    
                self.__yado_list_all_page.extend(self.__yado_list1)
                self.__yado_list1.clear()            
            else:
                self.__yado_list_all_page.extend(self.__yado_list1)          
                self.__yado_list1.clear()
                
                
        def scroll_down(self):
            #ページの高さを取得
            driver.execute_script("window.scrollTo(0, 1000);")
            #最後までスクロールすると長いので、半分の長さに割る。
            
            
        def repeat_next_page(self):
            
            area_yado_num = driver.find_element_by_xpath('//*[@id="search-tab"]/table[2]/tbody/tr[1]/td[1]/span[1]').text
            area_yado_num =float(area_yado_num)
            click_num = area_yado_num // 30.01
            
            self.scrapping_get_h2()
            self.delete_advertisement()
            
    #         ここの一行で広告の数を使っている。このおかげで最後のページも広告を消せる。advertisement_numをglobal変数に
    #         すれば良いのだが、なぜかできないので、yado_list1をglobal変数にしている。
            advertisement_num = yado_list1 - 30
            
            # 以下のif文は掲載順位が2ページだけの宿の処理
            if int(click_num) == 1:
                try:
                    driver.find_element_by_partial_link_text("次へ").click()
                except:
                    driver.find_element_by_class_name('karte-close').click()
                    
                    print("popアップ削除")
                    driver.find_element_by_partial_link_text("次へ").click()
                self.__yado_list1.clear()
                self.scrapping_get_h2()
                
                while advertisement_num > 0:
                    self.__yado_list1.pop(0)
                    advertisement_num += -1
                self.__yado_list_all_page.extend(self.__yado_list1)
                self.__yado_list1.clear()
            else:
                # 以下のif文は掲載順位が1ページだけの宿の処理
                if int(click_num) == 0:
                    advertisement_num = yado_list1- int(area_yado_num)
                    self.scrapping_get_h2()
                    
                    while advertisement_num > 0:
                        self.__yado_list1.pop(0)
                        advertisement_num += -1
                        
                    self.__yado_list_all_page.clear()
                    self.__yado_list_all_page.extend(self.__yado_list1)
                    self.__yado_list1.clear()
                    
                else:
                    for click in range(int(click_num)):

                        # 以下のif文は最後のページで広告を消す処理
                        if click == int(click_num) -1:
                            try:
                                driver.find_element_by_partial_link_text("次へ").click()
                            except:
                                driver.find_element_by_class_name('karte-close').click()
                                driver.find_element_by_partial_link_text("次へ").click()
                            
                            self.scrapping_get_h2()

                            while advertisement_num > 0:
                                self.__yado_list1.pop(0)
                                advertisement_num += -1
                            self.__yado_list_all_page.extend(self.__yado_list1)
                            self.__yado_list1.clear()

                        else:
                            try:
                                driver.find_element_by_partial_link_text("次へ").click()
                            except:
                                time.sleep(1)
                                driver.find_element_by_class_name('karte-close').click()
                                driver.find_element_by_partial_link_text("次へ").click()
                                
                            self.scrapping_get_h2()
                            self.delete_advertisement()
                            
                            

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝エリア移動＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

                            
                            
                    
        def yado_rank(self):
            rank_list = []
            yado_name_list = []


            for rank, yado_name in enumerate(self.__yado_list_all_page , start=1):
                rank_list.append(rank)
                yado_name_list.append(yado_name)
            yado_rank_dict = dict(zip(yado_name_list, rank_list))
            
            try:
                self.__ja_reviews_dic["掲載順位"] = yado_rank_dict[self.__ja_reviews_dic["宿名"]]
            except:
                self.__ja_reviews_dic["掲載順位"] = "0"
            
            self.__ja_reviews_dic["日付"] = str(datetime.date.today())
            print(self.__ja_reviews_dic)
            print(yado_rank_dict)

            self.preservation()
            print("\n")
            self.__reviews_list.clear()
            self.__yado_list_all_page.clear()
            self.__page_list.clear()
            
            
        def preservation(self):
            
            yado_name = self.__ja_reviews_dic["宿名"]
            area = self.__ja_reviews_dic["エリア"]
            rank = float(self.__ja_reviews_dic["掲載順位"])
            
            total_review = float(self.__ja_reviews_dic["総合評価"])
            room_score = float(self.__ja_reviews_dic["部屋"])
            bath_score = float(self.__ja_reviews_dic["風呂"])
            breakfast_score = float(self.__ja_reviews_dic["料理（朝食）"])
            dinner_score = float(self.__ja_reviews_dic["料理（夕食）"])
            service_score = float(self.__ja_reviews_dic["接客・サービス"])
            review＿number = float(self.__ja_reviews_dic["口コミ件数"])
            beautiful_score = float(self.__ja_reviews_dic["清潔感"])
            
            stay_overnight_lowest_price = self.__ja_reviews_dic["素泊まり最安値"]
            dinner_breakfast_lowest_price = self.__ja_reviews_dic["2食付き最安値"]
            
            
            print(dinner_breakfast_lowest_price)
            print(type(dinner_breakfast_lowest_price))
            print("--------")
            
            
            now = self.__ja_reviews_dic["日付"]
            print(now)
            
            # name = Yado.objects.get(name)
            # print(name)
            row_name = Yado(name=yado_name)
            print(row_name.name)
            print("--------------------")
            print(yado_name)
            try:
                row_name.save()
            except:
                print("重複していたので保存しない")
            
            #reviewsオブジェクトのnameは、リレーションしているので、Yadoオブジェクトから引っ張ってきた宿名だといけない
            review1 = Yado.objects.get(name=yado_name)
            row = reviews(beautiful_score=beautiful_score,
                          room_score=room_score,
                          bath_score=bath_score,
                          yado_name = yado_name,
                          breakfast_score=breakfast_score, 
                          service_score=service_score,
                          review＿number=review＿number,
                          total_review=total_review,
                          dinner_score=dinner_score,
                          area=area,
                          rank=rank,
                          stay_overnight_lowest_price=stay_overnight_lowest_price,
                          dinner_breakfast_lowest_price=dinner_breakfast_lowest_price,
                          created_at=now,
                          name=review1)
            row.save()
            
    Create = Create()
    a_func = Create.url_create()

    Create_func = Create.get_yado_info()
    print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    print("データベースに完了")


if __name__ == '__main__':
    jaget()
# エリアの順位
