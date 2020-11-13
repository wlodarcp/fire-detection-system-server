import socket


def create_sockets(cameras, HOST):
    sockets = {}
    for camera in cameras:
        sockets[camera] = create_socket_for_camera(camera, HOST)
    print(sockets)
    return sockets


def create_socket_for_camera(camera, HOST):
    (camera_id, port) = (camera.id, camera.port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created for camera {' + str(camera_id) + '} on port {' + str(port) + '}')
    s.bind((HOST, port))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')
    return s
