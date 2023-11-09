import os
import re
import sys
import time
#import chromedriver_binary
import requests
from selenium import webdriver

# *** main関数(実行は最下部) ***
def main():
    args=sys.argv

    url=args[1]
    # URLリスト中のURLの検証
    #validate_url(url_list)
    # ブラウジング
    print(url)
    browsing_urls(url)


# *** ブラウジングを実行する関数 ***
def browsing_urls(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # ブラウザを最大化
    #options.add_argument("--start-maximized")
    # 「Chromeは自動テストソフトウェアによって制御されています。」を消すためのオプションの指定
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    #print("\n===== start =====")
    driver.get(url)
    #for i, url in enumerate(url_list):
    #    # URLリスト全体中何個目のURLを表示しているかを出力
    #    print("  " + str(i+1) + "/" + str(len(url_list)))
    #    # URLにアクセス
    #    #for num in range(10):
    #     #   driver.get(url)
    #      #  print(str(num) + "/" + "10")
    #    driver.get(url)
        # ↓各URLに行いたい処理があればここで呼び出す関数を変更する
    #print("===== end =====\n")
    # 終了
    #time.sleep(1)
    driver.close()
    print("Complete\n")
    #sys.stdout.write("Complete")
# main関数の実行
main()