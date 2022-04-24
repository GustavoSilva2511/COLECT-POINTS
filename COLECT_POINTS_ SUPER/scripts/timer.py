from time import time


class Timer:
    def __init__(self):
        self.start_time = time()
        self.time = time() - self.start_time

    def get(self):
        return int(self.time)
