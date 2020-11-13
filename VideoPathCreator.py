import os
from datetime import datetime


def create_path_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def build_path_for_video(startup_date, camera_id):
    return str('videos/' + startup_date.strftime("%b-%d-%Y") + '/cam_' + str(camera_id) + '/')


def build_video_name_with_path(startup_date, camera_id):
    path = build_path_for_video(startup_date, camera_id)
    create_path_if_not_exists(path)
    current_date_time = datetime.now()
    video_path = str(path + str(current_date_time.strftime("started_at_%H.%M")) + '.avi')
    print("Video path: " + video_path)
    return video_path