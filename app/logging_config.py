"""
Logging configuration for the application.
This module should be imported before any other application modules.
"""

import logging


def setup_logging(level=logging.INFO):
    """
    Configure logging for the entire application.

    Args:
        level: Logging level (default: logging.INFO)
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        force=True,  # Override any existing configuration
    )
