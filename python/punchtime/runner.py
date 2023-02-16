"""punchtime runner.
This is the entrypoint for the Punchtime probe.
Use run() to run a pipeline.
"""
# can remove __future__ once py 3.10 the lowest supported version
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)


def run():
    """Run a probe. Punchtime's entrypoint.
    Be aware that Punchtime adds a NOTIFY - 25 custom log-level and notify()
    function to logging.
    """
    logger.debug("starting pypyr")

    logger.debug("stopping punchtime")