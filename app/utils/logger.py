# app/utils/logger.py
import logging
import sys


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    # Only configure if no handlers exist to prevent duplicate logs
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # TODO: Add classname, function name
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger


logger = setup_logger("vendor_platform")