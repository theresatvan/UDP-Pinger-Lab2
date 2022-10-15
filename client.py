from socket import *
import time
import sys

def ping(host, port):
    resps = []
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    
    for seq in range(1,11):
        # Send ping message to server and wait for response back
        # On timeouts, you can use the following to add to resps
        # resps.append((seq, ‘Request timed out’, 0))
        # On successful responses, you should instead record the server response and the RTT (must compute server_reply and rtt properly)
        # resps.append((seq, server_reply, rtt))
        
        #Fill in start
        begin = time.time()
        message = 'Ping {} {}'.format(seq, str(begin))
        clientSocket.sendto(message.encode(), (host, port))
        
        # Timeout after 1 second of no response
        if time.time() - begin > 1:
            resps.append((seq, 'Request timed out', 0))
            continue
        
        modifiedMessage, serverAddress = clientSocket.recv(1024)
        end = time.time()
        
        server_reply = modifiedMessage.decode()
        rtt = end - begin
        
        resps.append((seq, server_reply, rtt))
        #Fill in end
    
    clientSocket.close()
    
    return resps

if __name__ == '__main__':
    resps = ping('127.0.0.1', 12000)
    print(resps)