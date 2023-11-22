# deepfingerprinting
##データセットについて
アクセスするウェブサイトurlは以下の5つとする
1.https://www.google.com/
2.https://www.youtube.com/
3.https://www.amazon.co.jp/
4.https://www.twitter.com/
5.https://www.yahoo.co.jp/

各サイトに計500回アクセスし、合計で2500個のトレースを取得する
それを学習:検証:テスト=8:1:1になるように分割する
学習データセット:2000
検証データセット:250
テストデータセット:250

深層学習時のラベルとの対応は以下の通り
1↔︎www.google.com
2↔︎www.youtube.com
3↔︎www.amazon.co.jp
4↔︎www.twitter.com
5↔︎www.yahoo.co.jp

##深層学習について
学習はgooglecolabを用いて行う
新しい環境で行う場合は以下のコマンドを行なっておく
'''
!pip install tensorflow
!pip install keras
import os
os.chdir('/content/drive/My Drive/selenium/')
'''
実行時は以下を実行
'''
!python pico_df.py
'''
