import pickle
import socket
import struct

from threading import Thread
import cv2
import random

cameras = [[1, 8098], [2, 8010]]
HOST = 'localhost'

def create_sockets(cameras):
    sockets = []
    for camera in cameras:
        sockets.append(create_socket_for_camera(camera[0], camera[1]))
    return sockets        
        
def create_socket_for_camera(camera_id, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created for camera {' + str(camera_id) + '} on port {' + str(port) + '}')
    s.bind((HOST, port))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')
    return s


def listen_on_socket(socket):
    while True:
        conn, addr = socket.accept()     # Establish connection with client.
        on_new_client(conn)
    
def on_new_client(clientsocket):
    data = b'' ### CHANGED
    payload_size = struct.calcsize("L") ### CHANGED
    print('Welcome to the Server\n')
    randomId = str(random.randint(1, 1000))
    while True:
        while len(data) < payload_size:
            data += clientsocket.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += clientsocket.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

    # Extract frame
        frame = pickle.loads(frame_data)

    # Display
        cv2.imshow(str('frame' + randomId), frame)
        cv2.waitKey(1)
    clientsocket.stop()

if __name__ == "__main__":
    sockets = create_sockets(cameras)
    for socket in sockets:
        Thread(target = listen_on_socket,args = (socket,)).start()
    
