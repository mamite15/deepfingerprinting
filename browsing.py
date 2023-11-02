import os
import re
import sys
import time
import chromedriver_binary
import requests
from selenium import webdriver

# *** main関数(実行は最下部) ***
def main():
    # URL一覧ファイルの受付
    input_path = input_urls_file()
    # URLリストをファイルから取得
    url_list = get_url_list(input_path)
    # URLリスト中のURLの検証
    validate_url(url_list)
    # ブラウジング確認の受付
    confirm_browsing()
    # ブラウジング
    browsing_urls(url_list)


# *** URL一覧ファイルの入力を受け付ける関数 ***
def input_urls_file():
    print("\n########## Start processing ##########")
    print("Input filepath of urls : ")
    # ファイルの入力の受付(フルパス)
    input_path = input()
    print("\nCheck input file ...\n")
    # ファイルの存在チェック
    if os.path.exists(input_path):
        print('  [OK]: File exists. : ' + input_path)
    # ファイルが存在しない場合は終了
    else:
        print("  [ERROR]: File doesn't exist! : " + input_path)
        print("\nSystem Exit.\n")
        sys.exit()
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


# *** ブラウジング開始の入力を受け付ける関数 ***
def confirm_browsing():
    # Yes/No以外は無限ループ
    while True:
        print("\nStart browsing?  y/n  (default:y)")
        # 入力は全て小文字として受付(比較が楽)
        confirm_cmd = input().lower()
        # デフォルト(Enter)のみでもyとして扱う
        if ((confirm_cmd == "") or (confirm_cmd == "y")):
            break
        elif ((confirm_cmd == "n")):
            print("\nSystem Exit.\n")
            sys.exit()
        else:
            pass


# *** ブラウジングを実行する関数 ***
def browsing_urls(url_list):
    options = webdriver.ChromeOptions()
    # ブラウザを最大化
    options.add_argument("--start-maximized")
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
        driver.get(url)
        # ↓各URLに行いたい処理があればここで呼び出す関数を変更する
        # 各URLを最下部までスクロールする処理
        scrolle_to_end(driver)
    print("===== end =====\n")
    # 終了
    driver.quit()
    print("Complete.\n")


# *** ページの最下部までスクロールする関数 ***
def scrolle_to_end(driver):
    # スクロールする速さ(1以上を指定)
    SCROLL_SPEED = 3
    while not is_scrolle_end(driver):
        # 0.5秒待つ(基本的には不要だが読み込みが遅いときなどに使用する)
        # time.sleep(0.5)
        # 相対値でスクロール
        driver.execute_script("window.scrollBy(0, "+str(SCROLL_SPEED)+");")
    # 1秒待つ
    time.sleep(1)


# *** 一番下までスクロールしたか否か判定する関数 ***
def is_scrolle_end(driver):
    # 一番下までスクロールした時の数値を取得(window.innerHeight分(画面表示領域分)はスクロールをしないため引く)
    script = "return " + str(get_page_height(driver)) + \
        " - window.innerHeight;"
    page_most_bottom = driver.execute_script(script)
    # スクロール量を取得(ブラウザの種類やバージョンなどによって取得方法が異なる)
    script = "return window.pageYOffset || document.documentElement.scrollTop;"
    scroll_top = driver.execute_script(script)
    is_end = scroll_top >= page_most_bottom
    return is_end


# *** ページの高さを取得する関数 ***
def get_page_height(driver):
    # ブラウザのバージョンやサイトによって異なるため、最大値を取る
    # https://ja.javascript.info/size-and-scroll-window#ref-633
    # Tips:文字列を改行なしで複数行で書きたい場合には()で囲む
    script = ("return Math.max("
              "document.body.scrollHeight, document.documentElement.scrollHeight,"
              "document.body.offsetHeight, document.documentElement.offsetHeight,"
              "document.body.clientHeight, document.documentElement.clientHeight"
              ");")
    height = driver.execute_script(script)
    return height


# main関数の実行
main()