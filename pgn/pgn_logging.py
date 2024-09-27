import logging

logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])
logger = logging.getLogger("pgn_app")
logger.debug("logging started")
