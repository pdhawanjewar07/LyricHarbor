import time
import random

def human_delay(mean: float = 9.0, jitter: float = 0.3, minimum: float = 5.0):
    delay = random.gauss(mean, mean * jitter)
    time.sleep(max(minimum, delay))

