import logging


LOGGER_NAME = "llm_utility_lab"

def configure_logging() -> None:
    """Configure application-wide logging."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )


def get_logger(name: str | None = None) -> logging.Logger:
    """Return an application logger."""

    logger_name = (
        f"{LOGGER_NAME}.{name}"
        if name
        else LOGGER_NAME
    )

    return logging.getLogger(logger_name)
