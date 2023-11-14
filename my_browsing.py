import os
import re
import sys
import time
#import chromedriver_binary
import requests
import subprocess
from selenium import webdriver

# *** main関数(実行は最下部) ***
def main():
    # URL一覧ファイルの受付
    input_path = input_urls_file()
    # URLリストをファイルから取得
    url_list = get_url_list(input_path)
    # URLリスト中のURLの検証
    #validate_url(url_list)
    # ブラウジング
    browsing_urls(url_list)


# *** URL一覧ファイルの入力を受け付ける関数 ***
def input_urls_file():
    #print("\n########## Start processing ##########")
    #print("Input filepath of urls : ")
    # ファイルの入力の受付(フルパス)
    input_path = "test_url_list2.txt"
    #print("\nCheck input file ...\n")
    # ファイルの存在チェック
    #if os.path.exists(input_path):
    #    print('  [OK]: File exists. : ' + input_path)
    # ファイルが存在しない場合は終了
    #else:
    #    print("  [ERROR]: File doesn't exist! : " + input_path)
    #    print("\nSystem Exit.\n")
   #    sys.exit()
    return input_path


# *** URLリストをファイルから取得する関数 ***
def get_url_list(input_path):
    # ファイルのオープン
    targetFile = open(input_path)
    # 行ごとのURLのリスト
    url_list = targetFile.readlines()
    # ファイルのクローズ
    targetFile.close()
    return url_list

# *** ブラウジングを実行する関数 ***
def browsing_urls(url_list):
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    # ブラウザを最大化
    #options.add_argument("--start-maximized")
    # 「Chromeは自動テストソフトウェアによって制御されています。」を消すためのオプションの指定
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    cnt=0
    print("\n===== start =====")
    # 一行ずつブラウザを開く
    for i, url in enumerate(url_list):
    # URLリスト全体中何個目のURLを表示しているかを出力
        print("  " + str(i+1) + "/" + str(len(url_list)))
            #スクショファイル名指定
        cnt+=1
        file="image/screen" + str(cnt) + ".png"
        FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        print(FILEPATH)
        #tcpdump起動
        #pcapfile="pcap/" + str(cnt) + ".pcap"
        pcapfile="./pcap/image.pcap"
        password="Cookie!3777777\n".encode()
        tcpdump=subprocess.Popen(["sudo","-S","tcpdump","-i","enxcce1d50d3d69","-s","0","-w", pcapfile],input=password)
        # URLにアクセス
        #for num in range(10):
        #   driver.get(url)
        #  print(str(num) + "/" + "10")
        driver.get(url)
        # ページの幅指定
        w = driver.execute_script("return document.body.scrollWidth;")
        h = driver.execute_script("return document.body.scrollHeight;")
        # ウィンドウサイズセット
        driver.set_window_size(w,h)
    
        # スクショ撮影
        driver.save_screenshot(FILEPATH)
        tcpdump.kill()
    print("===== end =====\n")
    # 終了
    #time.sleep(1)
    print("Complete.\n")
    driver.close()
# main関数の実行
main()