import os
import re
import sys
import time
#import chromedriver_binary
import requests
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
    input_path = "test_url_list.txt"
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


# *** URLスキームとステータスコードを検証する関数 ***
def validate_url(url_list):
    print("\nCheck url scheme and status code ...\n")
    # エラーフラグ
    hasError = False
    for url in url_list:
        # Tips:readlines()で読み込んだ1行には改行コードがついてくるので削除
        unsafe_url = url.rstrip()
        # URLのスキームパターン
        URL_PTN = re.compile(r"^(http|https)://")
        # パターンに一致しない場合はエラー
        if not (URL_PTN.match(unsafe_url)):
            print("  [ERROR]: Url isn't valid! : " + unsafe_url)
            hasError = True
            # スキームが正しくない場合にはURLにリクエストしない
            continue
        # スキームが正しい場合にURLにリクエスト
        r = requests.get(unsafe_url)
        # ステータスコードが200(リダイレクトでも200)以外の場合はエラー
        if (r.status_code != 200):
            print("  [ERROR]: Status code isn't 200! : [" +
                  r.status_code + "]:" + unsafe_url)
            hasError = True
    # スキームが正しくない、またはステータスコードが200以外のものがあった場合には終了
    if hasError:
        print("\nSystem Exit.\n")
        sys.exit()
    print("  [OK]: All urls are valid and 200.")
    print("  [OK]: Number of urls : " + str(len(url_list)))


# *** ブラウジングを実行する関数 ***
def browsing_urls(url_list):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # ブラウザを最大化
    #options.add_argument("--start-maximized")
    # 「Chromeは自動テストソフトウェアによって制御されています。」を消すためのオプションの指定
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    print("\n===== start =====")
    # 一行ずつブラウザを開く
    for i, url in enumerate(url_list):
        # URLリスト全体中何個目のURLを表示しているかを出力
        print("  " + str(i+1) + "/" + str(len(url_list)))
        # URLにアクセス
        #for num in range(10):
         #   driver.get(url)
          #  print(str(num) + "/" + "10")
        driver.get(url)
        # ↓各URLに行いたい処理があればここで呼び出す関数を変更する
    print("===== end =====\n")
    # 終了
    driver.quit()
    print("Complete.\n")

# main関数の実行
main()