from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import csv
import random
from selenium.webdriver.common.by import By
import os
import sys
import time
import requests
from selenium.webdriver.chrome.options import Options
import pymysql
mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="",
    database="walmart"
)
mycursor = mydb.cursor()

mycursor.execute("Use Walmart")
mycursor.execute("Select * from urls")
mycursor2 = mydb.cursor()
mycursor2.execute('Use Walmart')
sql = "INSERT INTO Items (id, item_number,product_title,product_url,image_url,price) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE id=VALUES(id),product_title=VALUES(product_title),product_url=VALUES(product_url),image_url=VALUES(image_url),price=VALUES(price);"
urls=[]
for x in mycursor:
  urls.append(x[1])
mycursor2.execute('Use Walmart')
df=pd.read_csv('stores.csv')
total_pins=df['Store Zip'].tolist()
audioToTextDelay = 10
delayTime = 2
audioFile = "\\payload.mp3"
URL = "https://www.google.com/recaptcha/api2/demo"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"

def delay():
    time.sleep(random.randint(2, 3))

def audioToText(audioFile):
    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)

    delay()
    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result
def captch_solve():
    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="w_CQ w_CU w_CW"]'))
    )
    captcha=driver.find_element_by_css_selector('button[class="w_CQ w_CU w_CW"]')
    captcha.click()
    g_recaptcha = driver.find_elements_by_class_name('g-recaptcha')[0]
    outerIframe = g_recaptcha.find_element_by_tag_name('iframe')
    outerIframe.click()

    iframes = driver.find_elements_by_tag_name('iframe')
    audioBtnFound = False
    audioBtnIndex = -1

    for index in range(len(iframes)):
        driver.switch_to.default_content()
        iframe = driver.find_elements_by_tag_name('iframe')[index]
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(delayTime)
        try:
            audioBtn = driver.find_element_by_id("recaptcha-audio-button")
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception as e:
            pass

    if audioBtnFound:
        try:
            while True:
                # get the mp3 audio file
                src = driver.find_element_by_id("audio-source").get_attribute("src")
                print("[INFO] Audio src: %s" % src)

                # download the mp3 audio file from the source
                urllib.request.urlretrieve(src, os.getcwd() + audioFile)

                # Speech To Text Conversion
                key = audioToText(os.getcwd() + audioFile)
                print("[INFO] Recaptcha Key: %s" % key)

                driver.switch_to.default_content()
                iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
                driver.switch_to.frame(iframe)

                # key in results and submit
                inputField = driver.find_element_by_id("audio-response")
                inputField.send_keys(key)
                delay()
                inputField.send_keys(Keys.ENTER)
                delay()

                err = driver.find_elements_by_class_name('rc-audiochallenge-error-message')[0]
                if err.text == "" or err.value_of_css_property('display') == 'none':
                    print("[INFO] Success!")
                    break

        except Exception as e:
            print(e)
            sys.exit("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
    else:
        sys.exit("[INFO] Audio Play Button not found! In Very rare cases!")


def check_alertable():
    pass
def location_click():
        location=driver.find_element_by_xpath("//i[@class='ld ld-Location mr2']")
        location.click()
def zip_code_putter(array):
        current_pin=random.choice(array)
        print(current_pin)
        postal_clicker=WebDriverWait(driver, 5000).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="postalCode"]'))
        )
        postal_clicker.clear()
        postal_clicker.send_keys(current_pin)
        press=driver.find_element_by_xpath('//button[@form="update-postal-code-form"]')
        press.click()
all_data_scrapped=False
all_info=[]
while not(all_data_scrapped):
    try:
        for m in range(len(urls)):
            options = webdriver.ChromeOptions() 
            options.add_argument("start-maximized")
            driver = uc.Chrome(options=options)
            driver.get(urls[m])
            driver.implicitly_wait(30)
            location_clicked=False
            location_click()
            location_clicked=True
            if location_clicked is False:
                location_click()
            zip_code_putter(total_pins)
            time.sleep(3)
            no_of_pages_finder = driver.find_elements_by_xpath("//ul[@class='list flex items-center justify-center pa0']/li")
            total_pages=[]

            for i in no_of_pages_finder:
                total_pages.append(i.text)
            current_url_total_pages=(int(total_pages[-2]))
            current_url_info=[]
            total_no_of_results=driver.find_element_by_xpath('//span[@class="f6 f5-m fw3 ml1 gray normal self-center"]')
            no_of_results=total_no_of_results.text.replace('(','')
            no_of_results=no_of_results.replace(')','')
            no_of_results=no_of_results.replace('+','')
            no_of_results=int(no_of_results)
            if no_of_results>250:
                drop_down=driver.find_element_by_xpath('//button[@aria-label="Sort by Best Match"]')
                drop_down.click()
                time.sleep(2)
                select_from_field_for_low=driver.find_element_by_xpath('//label[@for="price_low"]')
                select_from_field_for_low.click()

            for j in range(((current_url_total_pages))):
                time.sleep(3)
                all_elements_in_page=(len(driver.find_elements_by_xpath('//div[@class="flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3"]/div')))
                print(all_elements_in_page)
                for i in range(1,(all_elements_in_page)+1):
                    info_current_product=[]
                    title_element_locator=f"//div[@class='flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3']/div[{i}]"
                    title_element=driver.find_element_by_xpath(title_element_locator)
                    title=title_element.text.splitlines()[0]
                    walmart_item_id_element_locator=f"//div[@class='flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3']/div[{i}]/div/div/a"
                    walmart_item_id_element=driver.find_element_by_xpath(walmart_item_id_element_locator)
                    walmart_item_id=(walmart_item_id_element.get_attribute('link-identifier'))
                    product_link_element_locator=f"//div[@class='flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3']/div[{i}]/div/div/a"
                    product_link_element=driver.find_element_by_xpath(product_link_element_locator)
                    product_link=product_link_element.get_attribute('href')
                    product_image_link_element_locator=f"//div[@class='flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3']/div[{i}]/div/div/div/div/div/div/img"
                    product_image_link_element=driver.find_element_by_xpath(product_image_link_element_locator)
                    product_image_link=product_image_link_element.get_attribute('src')
                    product_price_element_locator=f"//div[@class='flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3']/div[{i}]"
                    product_price_element=driver.find_element_by_xpath(product_price_element_locator)
                    for l in product_price_element.text.split():
                        if '$' in l:
                            product_price=l
                            break
                        else:
                            product_price='0.0'
                    product_price=product_price.replace('$','')
                    product_price=product_price.replace(',','')
                    product_price=float(product_price)
                    info_current_product.append(m+1)
                    info_current_product.append(walmart_item_id)
                    info_current_product.append(title)
                    info_current_product.append(product_link)
                    info_current_product.append(product_image_link)
                    info_current_product.append(product_price)
                    val = tuple(info_current_product)
                    check_alertable() 
                    mycursor2.execute(sql, val)
                    current_url_info.append(info_current_product)
                    all_info.append(info_current_product)
                    mydb.commit()
                try:
                    next_page=driver.find_element_by_xpath("//a[@data-testid='NextPage']")
                    next_page.click()
                    driver.implicitly_wait(30)
                except:
                    pass
                finally:
                    if (len(driver.find_elements_by_xpath('//div[@class="flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3"]/div')))==0:
                        driver.back()
                        driver.implicitly_wait(30)
                        info_current_product=[]
                        title_element_locator=f"//div[@class='flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3']/div[{i}]"
                        title_element=driver.find_element_by_xpath(title_element_locator)
                        title=title_element.text.splitlines()[0]
                        walmart_item_id_element_locator=f"//div[@class='flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3']/div[{i}]/div/div/a"
                        walmart_item_id_element=driver.find_element_by_xpath(walmart_item_id_element_locator)
                        walmart_item_id=(walmart_item_id_element.get_attribute('link-identifier'))
                        product_link_element_locator=f"//div[@class='flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3']/div[{i}]/div/div/a"
                        product_link_element=driver.find_element_by_xpath(product_link_element_locator)
                        product_link=product_link_element.get_attribute('href')
                        product_image_link_element_locator=f"//div[@class='flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3']/div[{i}]/div/div/div/div/div/div/img"
                        product_image_link_element=driver.find_element_by_xpath(product_image_link_element_locator)
                        product_image_link=product_image_link_element.get_attribute('src')
                        product_price_element_locator=f"//div[@class='flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3']/div[{i}]"
                        product_price_element=driver.find_element_by_xpath(product_price_element_locator)
                        for l in product_price_element.text.split():
                            if '$' in l:
                                product_price=l
                                break
                            else:
                                product_price='0.0'
                        product_price=product_price.replace('$','')
                        product_price=product_price.replace(',','')
                        product_price=float(product_price)
                        info_current_product.append(m+1)
                        info_current_product.append(walmart_item_id)
                        info_current_product.append(title)
                        info_current_product.append(product_link)
                        info_current_product.append(product_image_link)
                        info_current_product.append(product_price)
                        val = tuple(info_current_product)
                        check_alertable() 
                        mycursor2.execute(sql, val)
                        current_url_info.append(info_current_product)
                        all_info.append(info_current_product)
                        mydb.commit()
                        next_page=driver.find_element_by_xpath("//a[@data-testid='NextPage']")
                        next_page.click()
                        print('here')
            print(f'Data Extracted from Website no.{m+1} of url:{urls[m]}')
            driver.close()
        print(f"{len(all_info)} records updated or added")
        print('Completed!')
        all_data_scrapped=True
        if all_data_scrapped==True:
            break
        mydb.commit()
    except:
        captch_solve()
        
        
