import logging


logger = logging.getLogger("fainaz_clientiq.integration")


def log_step(step: str, **details) -> None:
    safe_details = {key: value for key, value in details.items() if value is not None}
    logger.info("%s | %s", step, safe_details)
