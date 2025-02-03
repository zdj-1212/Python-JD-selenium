import json
import random
import time
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By

def login(driver):
    url="http://www.jd.com/"
    try:
        with open("jdcookie.json","r",encoding="utf-8") as f:
            cookie=json.load(f)
            f.close()
    except:
        driver.get("https://passport.jd.com/uc/login")
        time.sleep(100)
        cookie=driver.get_cookies()
        with open("jdcookie.json","w",encoding="utf-8") as f:
            json.dump(cookie,f)
            f.close()
            print("cookie写入成功")
        cookie = json.load(cookie)
    driver.get(url)
    time.sleep(2)
    for i in cookie:
         driver.add_cookie(i)

def get_data(driver):
    data_to_save=[]
    page_num=1
    current_window = driver.current_window_handle
    window_handles = driver.window_handles
    for window in window_handles:
        if window != current_window:
            driver.switch_to.window(window)
    # ele=driver.find_element(By.XPATH,"""//div[@id='detail']//ul/li[@data-anchor='#comment']""")
    # res=ele.location_once_scrolled_into_view
    # print(f"滚动后的坐标:{res}")
    driver.find_element(By.XPATH, """//div[@id='detail']//ul/li[@data-anchor='#comment']""").click()
    while True:
        page_num=page_num+1
        time.sleep(2)
        print("正在获取data_list")
        data_list = driver.find_elements(By.XPATH,"""//div[@id="comment"]//div[@class="mc"]//div[@class="comment-item"]""")
        for data in data_list:
            try:
                print("正在获取username")
                username = data.find_element(By.XPATH, """.//div[@class="user-info"]""").text
            except:
                username = "N/A"
            try:
                print("正在获取comment")
                comment = data.find_element(By.XPATH,""".//div[@class='comment-column J-comment-column']/p[@class='comment-con']""").text
            except:
                comment = "N/A"
            try:
                print("正在获取spans")
                spans = data.find_elements(By.XPATH, """.//div[@class="order-info"]//span""")
            except:
                spans = "N/A"
            try:
                print("正在获取color")
                color = data.find_element(By.XPATH, """.//div[@class="order-info"]//span[1]""").text
            except:
                color = "N/A"
            try:
                print("正在获取model")
                model = data.find_element(By.XPATH, """.//div[@class="order-info"]//span[2]""").text
            except:
                model = "N/A"
            try:
                print("正在获取timestamp")
                timestamp = spans[-2].text
            except:
                timestamp = "N/A"
            try:
                print("正在获取address")
                address =spans[-1].text
            except:
                address = "N/A"
            try:
                print("正在获取star")
                star_div = data.find_element(By.XPATH, """./div[2]/div[1]""")
                star_name = star_div.get_attribute('class')
                star = star_name[-1] if star_name else ''
            except:
                star = "N/A"
            data_to_save.append({
                'Username': username,
                'Comment': comment,
                'Color': color,
                'Model': model,
                'Time': timestamp,
                'Address': address,
                'Star': star
            })
        try:
            # driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            # js="window.scrollBy(0,-500)"
            # for i in range(3):
            #     time.sleep(2)
            #     driver.execute_script(js)
            print("正在寻找下一页按钮")
            driver.find_element(By.XPATH,"""//div[@class='ui-page-wrap clearfix']/div[@class='ui-page']/a[@class='ui-pager-next'and@clstag]""").click()
        except:
            print("数据爬取完毕,共爬取{}条数据".format(str(page_num-1)))
            break

    df = pd.DataFrame(data_to_save)
    # 保存到 CSV 文件
    df.to_csv('JD_comments_data.csv', index=False, encoding='utf-8')
key=input("请输入要爬取的商品关键字:")
driver=webdriver.Chrome()
driver.implicitly_wait(30)
login(driver)
time.sleep(2)
driver.maximize_window()
url = (f"https://search.jd.com/Search?keyword={key}")
driver.get(url)
time.sleep(2)
driver.find_element(By.XPATH,"""//div[@id="J_goodsList"]/ul/li[3]/div/div/a/img""").click()
time.sleep(2)
get_data(driver)
driver.quit()