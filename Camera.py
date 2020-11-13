class Camera:
    cameras = []

    def __init__(self, id, port, has_fire_detection_enabled):
        self.id = id
        self.port = port
        self.has_fire_detection_enabled = has_fire_detection_enabled
        self.cameras.append(id)

    def __getitem__(self, key):
        return key

