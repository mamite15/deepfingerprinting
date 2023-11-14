import pyshark
import ipaddress
import numpy as np
import os
import glob
import nest_asyncio

def main():
    nest_asyncio.apply()
    dir=np.zeros((50,5000))
    web_number=0
    traffic_number=-1
    cnt=0
    dir_path="./scap/"
    file_list=glob.glob(os.path.join(dir_path,"*.pcap"))
    #print(file_list)
    for pcap_file in file_list:
        traffic_number+=1
        direction=0
        #print(pcap_file)
        cap=pyshark.FileCapture(pcap_file)
        #packet=cap[1506]
        #layer=packet[1]
        #print(layer.src)
        #print(layer.dst)
        print(cap)
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
                    cnt+=1
                    dir[traffic_number][direction]=1
                    #print(traffic_number)
                    direction+=1
                elif(ip.compressed != '192.168.10.150' and direction < 5000):
                    dir[traffic_number][direction]=-1
                    #print(traffic_number)
                    #if(direction < 5000):
                    direction+=1
                else:
                    break
            else:
                #print("6")
                ip = ipaddress.IPv6Address(hexdata.src)
                if(ip.compressed == 'fe80::83a6:4691:127b:adb9' and direction < 5000):
                    cnt+=1
                    dir[traffic_number][direction]=1
                    #print(traffic_number)
                    direction+=1
                elif(ip.compressed != 'fe80::83a6:4691:127b:adb9' and direction < 5000):
                    dir[traffic_number][direction]=-1
                    #print(traffic_number)
                    #if(direction < 5000):
                    direction+=1
                else:
                    break
        print(dir[traffic_number])
        #別のウェブサイトへのアクセスか判定
        #if()
    print(cnt)
    print(dir)
    cap.close()

main()