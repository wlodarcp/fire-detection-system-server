from collections import deque


class Camera:

    QUEUE_SIZE = 20
    FIRE_TIME_RATE = 0.9

    def __init__(self, id, port, has_fire_detection_enabled):
        self.id = id
        self.port = port
        self.has_fire_detection_enabled = has_fire_detection_enabled
        if self.has_fire_detection_enabled:
            self.fire_signal_queue = deque([False] * self.QUEUE_SIZE, maxlen=self.QUEUE_SIZE)

    def update_fire_signal_queue(self, fire_signal):
        if self.has_fire_detection_enabled:
            self.fire_signal_queue.appendleft(bool(fire_signal))

    def is_fire_detected_in_long_measurement(self):
        if self.has_fire_detection_enabled:
            return self.fire_signal_queue.count(True)/self.QUEUE_SIZE > self.FIRE_TIME_RATE
        return False
