import yaml
from attr import dataclass

from Camera import Camera


@dataclass
class Configuration:
    cameras: list
    is_video_saving_enabled: bool
    is_fire_detection_signal_check_enabled: bool
    HOST: str


def load_configuration(config_file_name):
    with open(config_file_name) as f:
        config = yaml.safe_load(f)
        loaded_cameras = load_cameras_from_config(config['cameras'])
        configuration = Configuration(loaded_cameras, config['is_video_saving_enabled'], config['is_fire_detection_signal_check_enabled'], config['HOST'])
        print(configuration)
        return configuration


def load_cameras_from_config(camera_list):
    cameras = []
    for camera in camera_list:
        cameras.append(Camera(camera['id'], camera['port'], camera['has_fire_detection_enabled']))
    return cameras
