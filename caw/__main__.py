import os
import logging

from caw.commands import app


if 'CAW_DEBUG' in os.environ:
    logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    app()
