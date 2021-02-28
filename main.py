'''
Lab for the HC-SR04 sensor.
'''
import sys
import logging
import time
from RPi import GPIO

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SPEED_OF_SOUND = 34300  # cm/s
PULSE_TIME = 0.00001
WARMUP_TIME = 0.5
ECHO = 26
TRIGGER = 20


class Sensor:
    def __init__(self):
        '''
        Initialize the Pi / Sensor things
        '''
        logger.debug('Sensor.__init__() called')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIGGER, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        time.sleep(WARMUP_TIME)

    def __del__(self):
        '''
        Cleanup the GPIO stuff on the way out.
        '''
        logger.debug('Sensor.__del__() called')
        GPIO.cleanup()

    def find_distance(self):
        '''
        Take a reading, first pulse the trigger for a brief moment and listen
        for the answer. Do some math. Profit
        '''
        GPIO.output(TRIGGER, 1)
        time.sleep(0.00001)
        GPIO.output(TRIGGER, 0)

        while GPIO.input(ECHO) == 0:
            pass
        start = time.time()

        while GPIO.input(ECHO) == 1:
            pass
        stop = time.time()

        self.elapsed_time = stop - start
        logger.info('elapsed time = %s', self.elapsed_time)
        return self.calc_distance()

    def calc_distance(self):
        return round(SPEED_OF_SOUND * (self.elapsed_time/2.0), 1)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='[%(levelname)s] %(asctime)s (%(module)s) %(message)s',
        datefmt='%Y/%m/%d-%H:%M:%S'
    )

    sensor = Sensor()
    distance = sensor.find_distance()
    logger.info('distance to something = %s cm', distance)
