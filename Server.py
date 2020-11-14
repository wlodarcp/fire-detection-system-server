import pickle
import struct
from datetime import date
from threading import Thread, Lock

import cv2
from flask import Flask
from flask import Response
from flask import render_template

from Configuration import load_configuration
from FireAlarmColorSelector import FireAlarmColorSelector
from SocketForCameraCreator import create_sockets
from VideoPathCreator import build_video_name_with_path

config = load_configuration('config.yaml')

cameras = config.cameras
is_video_saving_enabled = config.is_video_saving_enabled
is_fire_detection_signal_check_enabled = config.is_fire_detection_signal_check_enabled
HOST = config.HOST

startup_date = date.today()
image_on_camera_unavialable = cv2.imread(str('templates/broken_glass.jpg'), 1)

current_frames_from_cameras = {}
lock = Lock()

app = Flask(__name__)

color_selector = FireAlarmColorSelector()


def generate_video_stream_for_web_browser(camera_id):
    global lock, current_frames_from_cameras
    while True:
        # wait until the lock is acquired
        with lock:
            try:
                output = current_frames_from_cameras[int(camera_id)]
                (flag, encoded_image) = cv2.imencode(".jpg", output)
            except Exception as e:
                (flag, encoded_image) = cv2.imencode(".jpg", image_on_camera_unavialable)
            if not flag:
                continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n')


@app.route("/")
def index():
    return render_template("index.html", camera_list=cameras, is_fire_check_enabled=is_fire_detection_signal_check_enabled, fire_color_selector=color_selector)


@app.route("/video_feed/<camera_id>")
def video_feed(camera_id):
    return Response(generate_video_stream_for_web_browser(camera_id), mimetype="multipart/x-mixed-replace; boundary=frame")


def listen_on_socket(socket, camera):
    while True:
        conn, addr = socket.accept()  # Establish connection with client.
        on_new_client(conn, camera)


def is_day_changed():
    actual_date = date.today()
    return actual_date != startup_date


def update_vide_name_on_day_change(camera_id):
    global startup_date
    startup_date = date.today()
    return build_video_name_with_path(startup_date, camera_id)


def extract_signal_from_fire_detctor(clientsocket, data):
    received = clientsocket.recv(4096)
    if not received: raise Exception()
    data += received
    is_fire = data[0]
    data = data[1:]
    return data, is_fire


def find_camera_by_id(camera_id):
    return next((camera for camera in cameras if camera.id == camera_id), None)


def on_new_client(clientsocket, camera):
    camera_id = camera.id
    global lock, current_frames_from_cameras
    data = b''
    payload_size = struct.calcsize("L")
    print("Camera " + str(camera_id) + " CONNECTED to the server")
    vid_cod = cv2.VideoWriter_fourcc(*'XVID')
    video_name = build_video_name_with_path(startup_date, camera_id)
    output = None
    while True:
        try:
            if is_fire_detection_signal_check_enabled and camera.has_fire_detection_enabled:
                (data, is_fire) = extract_signal_from_fire_detctor(clientsocket, data)
                camera.update_fire_signal_queue(is_fire)
            while len(data) < payload_size:  # 1 because first byte is info about is fire signal
                received = clientsocket.recv(4096)
                if not received: raise Exception()
                data += received

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]  ### CHANGED

            # Retrieve all data based on message size
            while len(data) < msg_size:
                data += clientsocket.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            if is_day_changed():
                video_name = update_vide_name_on_day_change(camera_id)
                if output is not None and is_video_saving_enabled:
                    output.release()  # save previous video if day changed
            # Extract frame
            frame = pickle.loads(frame_data)
            with lock:
                current_frames_from_cameras[camera_id] = frame.copy()
            if output is None and is_video_saving_enabled:
                output = cv2.VideoWriter(video_name, vid_cod, 20.0, (frame.shape[1], frame.shape[0]))
            # Display
            #cv2.imshow(str('frame_for_camera-' + str(camera_id)), frame)
            #cv2.waitKey(1)
            if is_video_saving_enabled:
                output.write(frame)

        except Exception as e:
            print(e)
            print("Camera " + str(camera_id) + " DISCONNECTED")
            if is_video_saving_enabled:
                output.release()
            #cv2.destroyWindow(str('frame_for_camera-' + str(camera_id)))
            break


if __name__ == "__main__":
    sockets = create_sockets(cameras, HOST)
    for camera in sockets:
        Thread(target=listen_on_socket, args=(sockets[camera], camera,), daemon=True).start()
    app.run(host='localhost', port='1234', debug=True, threaded=True, use_reloader=False)
