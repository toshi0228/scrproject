from selenium import webdriver
import time
import pandas as pd
import re
import datetime


def rtsaget():
    print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    
    driver=webdriver.Chrome("./selenium/chromedriver")
    driver.maximize_window()


    key_list = ["宿名",'楽天番号','エリア',"日付",'掲載順位', '部屋数' , '総合評価', 'サービス', '立地', '部屋', '設備・アメニティ', '風呂','食事',
                "写真枚数",'アンケート件数', '内訳5点', '内訳4点','内訳3点', '内訳2点', '内訳1点']

    rt_dic_list = {}
    for key in key_list:
        rt_yado_dc = dict.fromkeys([key], '')

        rt_dic_list.update(rt_yado_dc)


    with open(str(datetime.date.today())+ "RT.csv", 'w', encoding='utf-8') as f:
        for key in key_list:
            f.write(str(key) + ",")
        f.write('\n')
        
        

    class review():

    # 掲載順位や順位を入れるリスト
        def __init__(self):
            
            # ※楽天番号
            self.__yados_num = []
            
            self.__reviews_list = []
            self.__yado_list_all_page = []
            self.__yado_rank = []
            self.__urls = []
            
            self.__rt_reviews_dic = rt_dic_list
        
        
        def url_create(self):
            
            #このファイルに楽天の番号を入れることによって、宿の口コミを取得できる。
            with open('./ys/RT_yado_num.txt', encoding='utf-8') as f:
                for row in f:
                    yado = row.rstrip()
                    self.__yados_num.append(yado)
                    
            for yado_num in self.__yados_num:
                global url
                url = ("https://travel.rakuten.co.jp/HOTEL/" + str(yado_num) + "/" + str(yado_num) + ".html")
                self.__urls.append(url)
            print(self.__urls)
    

        def access_get(self):
            for i, (num, url) in enumerate(zip(self.__yados_num, self.__urls),start=1):
                self.__rt_reviews_dic["楽天番号"] = num
                
                try:
                    self.__rt_reviews_dic["掲載順位"] = i
                except:
                    self.__rt_reviews_dic["掲載順位"] = "ー"
                    
                self.__rt_reviews_dic["日付"] = str(datetime.date.today())
                driver.get(url)
                time.sleep(1)
                
                #口コミを取得する前に部屋数を取得する
                self.movement_detail()
                
                try:
                    driver.find_element_by_partial_link_text("お客さまの声").click()
                    time.sleep(1)
                    reviews_table = driver.find_element_by_xpath('//*[@id="rateArea"]').text
                    
                except:    
                    pass
                
                self.__rt_reviews_dic["宿名"] = driver.find_element_by_xpath('//*[@id="RthNameArea"]/h2/a').text
                self.__rt_reviews_dic["エリア"] = driver.find_element_by_xpath('//*[@id="breadcrumbs-small"]/span').text
                
                self.picture_check()
                
                try:
                    # reは正規表現　split[\n :]で空白と：区切る
                    reviews = re.split('[\n："件"]',reviews_table)

                    # reviewsの中の必要ないものをここではき出す
                    for review in reviews:
                        if review == "5点" or review == "4点" or review == "3点" \
                            or review == "2点" or review == "1点" or review == "評価内訳" \
                            or review == "総合評価" or review == "アンケート" or review == "項目別の評価" \
                            or review == "サービス" or review == "立地" or review == "部屋" or review == "設備・アメニティ" \
                            or review == "風呂" or review == "食事" or review == "数" or review == '':
                            pass
                        else:
                            if review == "－－－－－":
                                review = review.replace("－－－－－","ー")
                            self.__reviews_list.append(review)
                except:
                    pass
                
                
                no_review = self.__rt_reviews_dic["宿名"].split('・')
                no_review = no_review[-1]
                if no_review == "ハピホテ提携】":
                    self.__reviews_list.clear()
                    
                    for review in range(13):
                        self.__reviews_list.append("ー")
                        
                else:
                    pass
                
                
                self.__rt_reviews_dic["総合評価"] = self.__reviews_list[0]
                self.__rt_reviews_dic["アンケート件数"] = self.__reviews_list[1]
                self.__rt_reviews_dic["内訳5点"] = self.__reviews_list[2]
                self.__rt_reviews_dic["内訳4点"] = self.__reviews_list[3]
                self.__rt_reviews_dic["内訳3点"] = self.__reviews_list[4]
                self.__rt_reviews_dic["内訳2点"] = self.__reviews_list[5]
                self.__rt_reviews_dic["内訳1点"] = self.__reviews_list[6]
                self.__rt_reviews_dic["サービス"] = self.__reviews_list[7]
                self.__rt_reviews_dic["立地"] = self.__reviews_list[8]
                self.__rt_reviews_dic["部屋"] = self.__reviews_list[9]
                self.__rt_reviews_dic["設備・アメニティ"] = self.__reviews_list[10]
                self.__rt_reviews_dic["風呂"] = self.__reviews_list[11]
                self.__rt_reviews_dic["食事"] = self.__reviews_list[12]
                

                self.__reviews_list.clear()
                print(self.__rt_reviews_dic)
                print("\n")
                
                
                self.preservation()
                
        def movement_detail(self):
            
            #カスタがない場合,詳細情報を押せないので、try,exceptを使う。
            try:
                driver.find_element_by_partial_link_text("詳細情報").click()
                room_num = driver.find_element_by_xpath('//*[@id="htlCntntArea"]/div/article[1]/ul/li[8]/dl/dd').text
                room_num = room_num.split("室")
                self.__rt_reviews_dic["部屋数"] = int(room_num[0])
            except:
                room_num = driver.find_element_by_xpath('//*[@id="htlCntntArea"]/div/article[1]/ul/li[8]/dl/dd').text
                room_num = room_num.split("室")
                self.__rt_reviews_dic["部屋数"] = int(room_num[0])            
                


                

    #==========================================掲載順位================================================


        
    # ここから掲載順位を見つける為の関数   
        
        def movement_area(self):
            area =driver.find_element_by_link_text(self.__rt_reviews_dic["エリア"]).text
            
            if area == "東京２３区内" or area == "大阪" or area == "京都" or area == "名古屋":
                self.__rt_reviews_dic["エリア"] = driver.find_element_by_xpath('//*[@id="breadcrumbs-detail"]/span').text
                driver.find_element_by_link_text(self.__rt_reviews_dic["エリア"]).click()
            else:
                driver.find_element_by_link_text(self.__rt_reviews_dic["エリア"]).click()
            
        def scrapping_get_h1(self):
            yado_list = []
            elements = driver.find_elements_by_tag_name('h1')
            for element in elements:
                yado_name = element.text
                if yado_name == "最近見た宿泊施設" or yado_name == "同じ施設を見た人はこんな施設も見ています":
                    pass
                else:
                    yado_list.append(yado_name)
            yado_list.pop(0)
            self.__yado_list_all_page.extend(yado_list)
            
            
    # この関数の中で、ページを移動と同時にh1タグを取得 h1タグ取得はページ移動したたびにself.scrapping_get_h1を呼び出す        
        def repeat_next_page(self):
            area_yado_num = driver.find_element_by_xpath('//*[@id="srchMainContent"]/div[2]/p/span/em').text
            area_yado_num =float(area_yado_num)
            click_num = area_yado_num // 30.01
            
            self.scrapping_get_h1()

            for click in range(int(click_num)):
                driver.find_element_by_partial_link_text("次の").click()
                self.scrapping_get_h1()
                
            
        def yado_rank(self):
            rank_list = []
            yado_name_list = []

            for rank, yado_name in enumerate(self.__yado_list_all_page , start=1):
                rank_list.append(rank)
                yado_name_list.append(yado_name)
                
            
            yado_rank_dict = dict(zip(yado_name_list, rank_list))
            
            try:
                self.__rt_reviews_dic["掲載順位"] = yado_rank_dict[self.__rt_reviews_dic["宿名"]]
            except:
                self.__rt_reviews_dic["掲載順位"] = "ー"
            self.__rt_reviews_dic["日付"] = str(datetime.date.today())
            
            print(self.__rt_reviews_dic)
            print("\n")
            
            self.preservation()
            self.__reviews_list.clear()
            self.__yado_list_all_page.clear()
            
            
            
    #==========================================掲載順位================================================
            
        
        def preservation(self):
            with open(str(datetime.date.today())+ "RT.csv", 'a', encoding='utf-8') as f:
                for review_list in self.__rt_reviews_dic.values():
                    f.write(str(review_list) + ",")
                f.write('\n')    
                
                    
        def picture_check(self):
            try:
                picture = driver.find_element_by_xpath('//*[@id="navPht"]/a').text
                picture = (re.split('[()]', picture))

                for picture_num in picture:
                    if picture_num == "写真・動画" or picture_num == '':
                        pass
                    else:
                        self.__rt_reviews_dic["写真枚数"] = picture_num
            except:
                self.__rt_reviews_dic["写真枚数"] = "ー"
                    
            
            
    kyosen = review()
    kyosen.url_create()
    kyosen.access_get()



    print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    print("完了")
    driver.quit()
    
    
if __name__ == '__main__':
    rtsaget()
