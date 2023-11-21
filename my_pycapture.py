import pyshark
import ipaddress
import numpy as np
import os
import glob
import nest_asyncio
import re
import pickle

def main():
    nest_asyncio.apply()
    vec=np.zeros((500,5000))
    traffic_number=0
    cnt=0
    domain=np.zeros(500)
    #読み取るpcapファイル指定
    dir_path="./pcap/"
    file_list=glob.glob(os.path.join(dir_path,"*.pcap"))
    #1つずつ読み取って解析
    for pcap_file in file_list:
        direction=0
        cap=pyshark.FileCapture(pcap_file,display_filter="(tcp.port == 443) or (udp.port == 443)")
        print(str(cap) + "の解析")
        sp=re.split("[/_]",str(cap))
        #print(traffic_number)
        print(str(sp[1]))
        if(str(sp[1]) == "www.google.com"):
            domain[traffic_number]=1
        elif(str(sp[1]) == "www.youtube.com"):
            domain[traffic_number]=2
        elif(str(sp[1]) == "www.amazon.co.jp"):
            domain[traffic_number]=3
        elif(str(sp[1]) == "www.twitter.com"):
            domain[traffic_number]=4
        else:
            domain[traffic_number]=5
        
        for packet in cap:
            #packet=cap[item]
            hexdata=packet[1]
            #print(packet[1])
            #print(hexdata.src)
            #送信元が自分自身なら1,そうでないなら-1をdirにいれる
            if(hexdata.version == '4'):
                #print("4")
                ip = ipaddress.IPv4Address(hexdata.src)
                if(ip.compressed == '192.168.10.150' and direction < 5000):
                #if(ip.compressed == '192.168.3.9' and direction < 5000):
                    cnt+=1
                    vec[traffic_number][direction]=1
                    #print(traffic_number)
                    direction+=1
                elif(ip.compressed != '192.168.10.150' and direction < 5000):
                #elif(ip.compressed != '192.168.3.9' and direction < 5000):
                    vec[traffic_number][direction]=-1
                    #print(traffic_number)
                    #if(direction < 5000):
                    direction+=1
                else:
                    break
            else:
                #print("6")
                ip = ipaddress.IPv6Address(hexdata.src)
                if(ip.compressed == 'fe80::cee1:d5ff:fe0d:3d69' and direction < 5000):
                #if(ip.compressed == '2400:2650:6183:f000:68da:4cb3:55a5:6358' and direction < 5000):
                    cnt+=1
                    vec[traffic_number][direction]=1
                    #print(traffic_number)
                    direction+=1
                elif(ip.compressed != 'fe80::cee1:d5ff:fe0d:3d69' and direction < 5000):
                #elif(ip.compressed != '2400:2650:6183:f000:68da:4cb3:55a5:6358' and direction < 5000):
                    vec[traffic_number][direction]=-1
                    #print(traffic_number)
                    #if(direction < 5000):
                    direction+=1
                else:
                    break
        print("特徴")
        print(vec[traffic_number])
        print("ラベル")
        print(domain[traffic_number])
        print()
        traffic_number+=1
    
    cap.close()
    print("結果:")
    print("特徴")
    print(vec)
    print("ラベル")
    print(domain)
    pkl(traffic_number,vec,domain)

def pkl(traffic_number,vec,domain):
    x_train_file = "pickle/x_train.pkl"
    y_train_file = "pickle/y_train.pkl"
    x_valid_file = "pickle/x_valid.pkl"
    y_valid_file = "pickle/y_valid.pkl"
    x_test_file = "pickle/x_test.pkl"
    y_test_file = "pickle/y_test.pkl"
    
    
    a=traffic_number//10
    train_number=a*8
    valid_number=(traffic_number-train_number)//2
    test_number=traffic_number-valid_number-train_number
    print("総データ数:" + str(traffic_number))
    print("訓練データ数:" + str(train_number))
    print("検証データ数:" + str(valid_number))
    print("テストデータ数:" + str(test_number))
    x_train, x_valid, x_test = np.split(vec,[train_number,train_number+valid_number])
    y_train, y_valid, y_test = np.split(domain,[train_number,train_number+valid_number])
    #特徴量データをバイナリファイルに書き込み
    with open(x_train_file,"wb") as xtr:
        pickle.dump(x_train,xtr)
    with open(x_valid_file,"wb") as xv:
        pickle.dump(x_valid,xv)
    with open(x_test_file,"wb") as xte:
        pickle.dump(x_test,xte)
    #ラベルをバイナリファイルに書き込み
    with open(y_train_file,"wb") as ytr:
        pickle.dump(y_train,ytr)
    with open(y_valid_file,"wb") as yv:
        pickle.dump(y_valid,yv)
    with open(y_test_file,"wb") as yte:
        pickle.dump(y_test,yte)
main()