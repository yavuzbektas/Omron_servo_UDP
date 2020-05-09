import socket



#################### setting ###################
REMOTE_UDP_IP_ADDRESS = "192.168.0.131"
REMOTE_UDP_PORT_NO = 6000
LOCAL_UDP_IP_ADDRESS = "192.168.0.100"
LOCAL_UDP_PORT_NO = 6002

def send_message(Message):

    # Message = bytes(Message)
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSock.sendto(Message, (REMOTE_UDP_IP_ADDRESS, REMOTE_UDP_PORT_NO))

def recieve_message():
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSock.bind((LOCAL_UDP_IP_ADDRESS, LOCAL_UDP_PORT_NO))

    try:
        data, addr = serverSock.recvfrom(16)
        print("Message: ", list(data))
        return data
    except:
        return None

