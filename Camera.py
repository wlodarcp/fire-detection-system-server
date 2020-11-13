from collections import deque


class Camera:

    def __init__(self, id, port, has_fire_detection_enabled):
        self.id = id
        self.port = port
        self.has_fire_detection_enabled = has_fire_detection_enabled
        if self.has_fire_detection_enabled:
            self.fire_signal_queue = deque([False] * 20, maxlen=20)

    def __getitem__(self, key):
        return key

    def update_fire_signal_queue(self, fire_signal):
        if self.has_fire_detection_enabled:
            self.fire_signal_queue.appendleft(fire_signal)

    def is_fire_detected_in_long_measurement(self):
        if self.has_fire_detection_enabled:
            return self.fire_signal_queue.count(True)/20 > 0.5
        return False
