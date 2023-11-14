#!/bin/bash

cnt=1
for i in {1..10}
do
    while read line
    do
        echo $cnt
        sudo tcpdump -s 0 -U -w ./pcap/$cnt.pcap -W1 -G4 port 443&
        python browser_usingshell.py $line

        #python browser_usingshell.py $line &
        #sudo tcpdump -s 0 -U -w ./scap/$cnt.pcap port 443 

        if [ $? -eq 0 ]; then
            let cnt=$cnt+1
            #sudo kill $!
            wait $!
        #echo $line
        fi
    done < ./test_url_list.txt
done