import structlog
import logging

def configure_logging():
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ]
    )

    logging.basicConfig(level=logging.INFO)
    return structlog.get_logger()

logger = configure_logging()
