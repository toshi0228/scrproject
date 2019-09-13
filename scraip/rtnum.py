from selenium import webdriver
import time
import pandas as pd
import re
import datetime

def rtnum_get():
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    driver=webdriver.Chrome("/Users/enokitoshiki/anaconda3/envs/testskyper/selenium/chromedriver", chrome_options=chrome_options)
    driver.maximize_window()
    # --------------------------------------------------------------------------------リスト取得-------------------------------------------------------------------------------------

    class create():
        
        def __init__(self):
            
            #URLは、textからか取得したURL
            self.urls = [ ]
            
            #エリア全ページ分の宿名が入っている。
            self.yado_list_all_page = [ ]
            
            #宿名をクリックしてから、得られるURL　※実際は加工された後の宿番号だけが入る。
            self.get_urls = [ ]
            
            
        def url_create(self):
            
            #楽天番号
            yados_num = [ ]
            
            with open('/Users/enokitoshiki/Desktop/RT_yado_num.txt', encoding='utf-8') as f:
                for row in f:
                    yado = row.rstrip()
                    yados_num.append(yado)

            for yado_num in yados_num:
                global url
                url = ("https://travel.rakuten.co.jp/HOTEL/" + str(yado_num) + "/" + str(yado_num) + ".html")
                self.urls.append(url)
            print(self.urls)


        def access_get(self):

            for url in self.urls:
                driver.get(url)
                self.movement_area()
                create.repeat_next_page()
                
                self.all_page_check()
                self.yado_list_all_page.clear()

    # --------------------------------------------------------------------------------リスト取得-------------------------------------------------------------------------------------



    # --------------------------------------------------------------------エリア移動と宿名取得-----------------------------------------------------------------------------------


    # ここから掲載順位を見つける為の関数   
        
        def movement_area(self):
            
            area = driver.find_element_by_xpath('//*[@id="breadcrumbs-small"]/span').text
            
            if area == "東京２３区内" or area == "大阪" or area == "京都":
                area = driver.find_element_by_xpath('//*[@id="breadcrumbs-detail"]/span').text
                driver.find_element_by_xpath('//*[@id="breadcrumbs-detail"]/span').click()
            else:
                driver.find_element_by_xpath('//*[@id="breadcrumbs-small"]/span').click()
                
                
        #１ページの宿名を取得する関数
        def scrapping_get_h1(self):
            
            #宿の名前を入れるリスト
            yado_list = []
            
            elements = driver.find_elements_by_tag_name('h1')
            for element in elements:
                yado_name = element.text
                if yado_name == "最近見た宿泊施設" or yado_name == "同じ施設を見た人はこんな施設も見ています":
                    pass
                else:
                    yado_list.append(yado_name)
            yado_list.pop(0)
            self.yado_list_all_page.extend(yado_list)
            

    # この関数の中で、ページを移動と同時にh1タグを取得 h1タグ取得はページ移動したたびにself.scrapping_get_h1を呼び出す        
        def repeat_next_page(self):
            
            #area_yado_numは、エリアの宿件数
            area_yado_num = driver.find_element_by_xpath('//*[@id="srchMainContent"]/div[2]/p/span/em').text
            
            area_yado_num =float(area_yado_num)
            
            global click_num
            click_num = area_yado_num // 30.01
            print(click_num)
            
            self.scrapping_get_h1()

            for click in range(int(click_num)):
                driver.find_element_by_partial_link_text("次の").click()
                self.scrapping_get_h1()
            
            
    # --------------------------------------------------------------------エリア移動と宿名取得-----------------------------------------------------------------------------------



    # --------------------------------------------------------------------一件一件宿名クリック-----------------------------------------------------------------------------------
            
        def all_page_check(self):
            
            if click_num == 0:
                print("１はクリックしない")
            else:
                next_page = driver.find_element_by_partial_link_text("1").click()
            
            print("ここまでは大丈夫")
    #         embed()       
            
            
            #宿名をクリックさせる処理を行い、なければ次のページを押す
            global yado_name
            for i, yado_name,  in enumerate(self.yado_list_all_page, start = 1):
                try:
                    print(i)
                    self.yado_click()
                except:
                    print("except", i)
                    driver.find_element_by_partial_link_text("次の").click()
                    self.yado_click()
                    
            print(self.get_urls)
                    

        def yado_click(self):
            
            next_page = driver.find_element_by_partial_link_text(yado_name).click()
            print(driver.current_url)
            get_url = driver.current_url
            
            #取得したURLをスラッシュごとに分割"する。例）'https://travel.rakuten.co.jp/HOTEL/18214/18214.html'
            get_url = get_url.split('/')
            print(get_url[4])
            
            self.get_urls.append(get_url[4])
            
            time.sleep(1)
            driver.back()

            
        def preservation(self):
            with open(str(datetime.date.today())+ "RT_number.txt", 'w', encoding='utf-8') as f:
                for get_url in self.get_urls:
                    f.write(str(get_url) + "\n")
            


    create = create()
    create.url_create()
    create.access_get()
    create.preservation()



    driver.quit()
    print("完了")
    
if __name__ == '__main__':
    rtnum_get()