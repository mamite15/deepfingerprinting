import os
import re
import sys
import time
#import chromedriver_binary
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# *** main関数(実行は最下部) ***
def main():
    # URL一覧ファイルの受付
    #sys.path.append("/home/r-tao/.local/lib/python3.8/site-packages/selenium")
    input_path = "test_url_list.txt"
    # URLリストをファイルから取得
    url_list = get_url_list(input_path)
    # URLリスト中のURLの検証
    #validate_url(url_list)
    # ブラウジング
    browsing_urls(url_list)

# *** URLリストをファイルから取得する関数 ***
def get_url_list(input_path):
    # ファイルのオープン
    targetFile = open(input_path)
    # 行ごとのURLのリスト
    url_list = targetFile.readlines()
    # ファイルのクローズ
    targetFile.close()
    return url_list

def perform_actions(driver,keys):
    actions=ActionChains(driver)
    actions.send_keys(keys)
    time.sleep(2)
    print("Performing Actions")
    actions.perform()

def delete_cache(driver):
        #driver.execute_script("window.open('')")
        #driver.switch_to.window(driver.window_handles[-1])
        driver.get("chrome://settings/clearBrowserData")
        #perform_actions(driver,Keys.TAB*2 + Keys.DOWN*4 +Keys.TAB*5 + Keys.ENTER)
        perform_actions(driver,Keys.TAB + Keys.ENTER)
        #driver.close()
        #driver.switch_to.window(driver.window_handles[0])

# *** ブラウジングを実行する関数 ***
def browsing_urls(url_list):
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    # ブラウザを最大化
    #options.add_argument("--start-maximized")

    options.add_argument('--disable-gpu')
    # シークレットモードでの実行
    #options.add_argument('--incognito')
    
    #キャッシュを無効
    #options.add_argument('--disable-cache')
    #options.add_argument('--disable-application-cache')
    #options.add_argument("--disk-cache-size=0")
    #options.add_argument("--clear-cache")

    # 「Chromeは自動テストソフトウェアによって制御されています。」を消すためのオプションの指定
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    #delete_cache(driver)

    #driver.execute_cdp_cmd("Network.setCacheDisabled",{"cacheDisabled":True})

    #最大読み込み時間設定
    wait=WebDriverWait(driver=driver,timeout=130)
    print("\n===== start =====")
    # 一行ずつブラウザを開く
    for num in range(100):
        for url in url_list:
            #driver = webdriver.Chrome(options=options)
            ##最大読み込み時間設定
            #wait=WebDriverWait(driver=driver,timeout=30)
            domain=urlparse(url).netloc
            print(domain + "へのアクセス" + str(num+1) + "回目")
            file="image/" + domain + "_" + str(num+1) + ".png"
            FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
            #print(FILEPATH)
        #tcpdump起動
            pcapfile="./pcap/" + domain + "_" + str(num+1) + ".pcap"
            #subprocess.Popen(["sudo","tcpdump","-i","en5","-w",pcapfile])
            subprocess.Popen(["sudo","tcpdump","-i","enxcce1d50d3d69","-w", pcapfile])
        # URLにアクセス
            try:
                driver.get(url)

        #要素が全てくるまで待機
                wait.until(EC.presence_of_all_elements_located)
        # スクショ撮影
                #time.sleep(5)
                driver.save_screenshot(FILEPATH)

        #tcpdump停止
                subprocess.run(["sudo","pkill","tcpdump"])
                print()

                #不正アクセスと見做されないように時間を空ける
                time.sleep(10)
                #driver.close()
                #キャッシュ、クッキー全削除
                #driver.delete_all_cookies()
                delete_cache(driver)
                #time.sleep(30)
                #print("next")

            except Exception as e:
                print(e)
                print("error発生")
    print("===== end =====\n")
    # 終了
    print("Complete.\n")
    driver.close()
# main関数の実行
main()