"""
Logging configuration for the application.
This module should be imported before any other application modules.
"""

import logging


def setup_logging():
    """Configure logging for the entire application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


setup_logging()
