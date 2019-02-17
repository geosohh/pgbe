import logging


class Log:

    logger = None
    debugModeActive = False

    def __init__(self, debugModeActive: bool = None):
        if self.logger is None:
            self.logger = logging.getLogger("pgbe")
            # log_handler = logging.NullHandler()
            log_handler = logging.FileHandler("pgbe.log", mode="w")
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            log_handler.setFormatter(formatter)
            self.logger.addHandler(log_handler)
            self.logger.setLevel(logging.DEBUG)
            # self.logger.setLevel(logging.ERROR)

        if debugModeActive is not None:
            self.debugModeActive = debugModeActive

    def setDebugMode(self, debugModeActive: bool):
        self.debugModeActive = debugModeActive

    def debug(self,  msg, *args, **kwargs):
        if self.debugModeActive:
            if len(args) > 0 and len(kwargs) > 0:
                self.logger.debug(msg, args, kwargs)
            else:
                self.logger.debug(msg)

    def info(self, msg, *args, **kwargs):
        if self.debugModeActive:
            self.logger.info(msg, args, kwargs)
