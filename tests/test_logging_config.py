import logging

from src.logging_config import (
    LOGGER_NAME,
    configure_logging,
    get_logger,
)


def test_get_logger_uses_application_name():
    logger = get_logger()

    assert logger.name == LOGGER_NAME


def test_get_logger_creates_child_logger():
    logger = get_logger("client")

    assert logger.name == f"{LOGGER_NAME}.client"


def test_get_logger_returns_logging_instance():
    logger = get_logger("test")

    assert isinstance(logger, logging.Logger)


def test_configure_logging_sets_info_level(monkeypatch):
    configure_logging()

    root_logger = logging.getLogger()

    assert root_logger.level == logging.INFO
