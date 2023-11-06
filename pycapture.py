import pyshark
import ipaddress
import numpy as np

def main():
    cap=pyshark.FileCapture('d.pcap')
    dir=np.zeros((500,5000))
    web_number=0
    direction=0
    #packet=cap[1506]
    #layer=packet[1]
    #print(layer.src)
    #print(layer.dst)
    cnt=0
    for packet in cap:
        #packet=cap[item]
        layer=packet[1]
        #print(layer.src)
        #送信元が自分自身なら1,そうでないなら-1をdirにいれる
        ip = ipaddress.IPv4Address(layer.src)
        if(ip.compressed == '192.168.10.150'):
            cnt+=1
            dir[web_number][direction]=1
            direction+=1
        else:
            dir[web_number][direction]=-1
            direction+=1
        #別のウェブサイトへのアクセスか判定
        #if()
    print(cnt)
    print(dir)
    cap.close()

main()