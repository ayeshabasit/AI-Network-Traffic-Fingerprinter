import dpkt
import socket

f = open("Facebook1.pcap")
pcap = dpkt.pcap.Reader(f)

UUBCount = 1
UUBSize = 0
DUBCount = 1
DUBSize = 0
lastAddr = "10.103.104.34"
lastTime = 0
pCount = 1

with open('BurstCount.txt', 'a') as BC, open('BurstSize.txt', 'a') as BS, open('BurstTime.txt', 'a') as BT, open('packetFeatures.txt', 'a') as p:

    for ts, buf in pcap:
        # Packet Features (just length and direction for now)

#        p.write(str(pCount) + ': ' + str(len(buf)) + ' ')
        p.write(str(len(buf)) + ' ')
#	pCount+=1

        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        dstIpAddr = socket.inet_ntoa(ip.dst)
        srcIpAddr = socket.inet_ntoa(ip.src)

	# Burst features
        if lastTime == 0:
            initTime = ts

        if srcIpAddr == "10.103.104.34":
            p.write('>' + '\n')
            if lastAddr != "10.103.104.34":
		print "downlink uni burst count = ", DUBCount
                print "downlink uni burst size = ", DUBSize
                print "downlink uni burst time = ", lastTime - initTime

#                file.write("uplink uni burst count = " + str(UUBCount) + "\n")
#                file.write("uplink uni burst size = " + str(UUBSize) + "\n")
#                file.write("uplink uni burst time = " + str(lastTime - initTime) + "\n")

                BC.write(str(UUBCount) + "\n")
                BS.write(str(UUBSize) + "\n")
                BT.write(str(lastTime - initTime) + "\n")

                initTime = ts
                DUBCount = 0
                DUBSize = 0

            print "---->"
            UUBCount+=1
	    UUBSize+=len(buf)
        else:
            p.write('<' + '\n')
            if lastAddr == "10.103.104.34":
                p.write('<' + '\n')
                print "uplink uni burst count = ", UUBCount
                print "uplink uni burst size = ", UUBSize
                print "uplink uni burst time = ", lastTime - initTime

#                file.write("uplink uni burst count = " + str(UUBCount) + "\n")
#                file.write("uplink uni burst size = " + str(UUBSize) + "\n")
#                file.write("uplink uni burst time = " + str(lastTime - initTime) + "\n")

                BC.write(str(UUBCount) + "\n")
                BS.write(str(UUBSize) + "\n")
                BT.write(str(lastTime - initTime) + "\n")

                initTime = ts
                UUBCount = 1
                UUBSize = 0
            print "<----"
            DUBCount+=1
            UUBSize+=len(buf)

        lastAddr = srcIpAddr
        lastTime = ts
