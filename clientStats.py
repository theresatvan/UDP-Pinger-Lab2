from socket import *
import time
import sys

def ping(host, port):
    
    resps = []
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    
    for seq in range(1,11):
        clientSocket.settimeout(1)
        
        begin = time.time()
        message = "Ping {0} {1}".format(str(seq), str(begin))
        
        clientSocket.sendto(message.encode(), (host, port))
        
        try:
            modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
            end = time.time()
            
            server_reply = modifiedMessage.decode()
            rtt = end - begin
            
            resps.append((seq, server_reply, rtt))
            
        except timeout:
            resps.append((seq, 'Request timed out', 0))
    
    clientSocket.close()
    
    return resps

if __name__ == '__main__':
    resps = ping('127.0.0.1', 12000)
    print(resps, "\n")
    
    maxRTT = averageRTT = packetLoss = packetReceived = 0
    minRTT = sys.maxsize
    
    for response in resps:
        rtt = response[2]
        message = response[1]
        
        maxRTT = max(maxRTT, rtt)
        
        if message != "Request timed out":
            minRTT = min(minRTT, rtt)
            averageRTT += rtt
            packetReceived += 1
        else:
            packetLoss += 1
            
    packetLoss = (packetLoss / len(resps)) * 100
    
    if packetLoss == 100:
        minRTT = 0
    else:
        averageRTT = (averageRTT / packetReceived) * 1000
        maxRTT *= 1000
        minRTT *= 1000
        
    print("{} packets transmitted, {} packets received, {:.1f}% packet loss".format(len(resps), packetReceived, packetLoss))
    print("round-trip min/avg/max = {:.3f}/{:.3f}/{:.3f} ms".format(minRTT, averageRTT, maxRTT))