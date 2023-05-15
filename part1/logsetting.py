from utils import *

def setfunction(lenom : str):

        # setting up the logging object
    logger = logging.getLogger(lenom)
    logging.basicConfig(
            format='[%(asctime)s] [%(levelname)s] - %(message)s',
            datefmt='%H:%M:%S'
        )
        # we can change the logging level. Use logging.DEBUG if necesarry
    logger.setLevel(logging.DEBUG)
    return logger
