# -*- coding: utf-8 -*-
"""
    汎用ロガー
    (C) Masayuki Kanai 2022/02/22
"""

from logging import Formatter, handlers, getLogger, DEBUG, StreamHandler

class ProjectLogger:
    def __init__(self, filename, name=__name__):
        self.logger = getLogger(name)
        self.logger.setLevel(DEBUG)
        formatter = Formatter("[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s")
        try:
            # file
            handler = handlers.RotatingFileHandler(filename=filename, maxBytes=10485760, backupCount=5)
            # handler = handlers.TimedRotatingFileHandler(filename=filename, when='midnight', backupCount=7)
            handler.setLevel(DEBUG)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        except Exception:
            # stdout
            handler = StreamHandler()
            handler.setLevel(DEBUG)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
