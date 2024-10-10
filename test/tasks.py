###############################################################################
#
# Proprietary Information
#
# The information contained in this document is the property of Spirent
# Communications plc. Except as specifically authorised in writing by Spirent
# Communications plc, the holder of this document shall keep all information
# contained herein confidential and shall protect same in whole or in part
# from disclosure and dissemination to all third parties to the same degree
# it protects its own confidential information.
#
# (C) COPYRIGHT SPIRENT COMMUNICATIONS PLC 2024 - 2024
#
###############################################################################

import logging
import os
import sys

from invoke import task
from pathlib import Path

###############################################################################
# GLOBAL CONSTANTS
###############################################################################

SCRIPT_VERSION = "0.1"

SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_DIR = SCRIPT_PATH.parent

###############################################################################
# GLOBAL VARIABLES
###############################################################################

pass

###############################################################################
# LOCAL HELPER FUNCTIONS
###############################################################################


def configure_root_logger(debug=False) -> logging.Logger:
    """
    Configure the root logger with new handlers

    If debug is set, debugging output is enabled (default is disabled)

    Returns reference to root logger
    """
    logger = logging.getLogger()

    # As logger may already exist, ensure any existing handlers
    # are removed before adding our own
    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])

    # Set logging level and console formatting, depending on
    # value of param 'debug'
    if debug:
        logger.setLevel(logging.DEBUG)
        console_format_str = (
            "[%(asctime)s] [%(levelname)s] %(module)s->%(funcName)s() "
            "line %(lineno)d: %(message)s"
        )
    else:
        logger.setLevel(logging.INFO)
        console_format_str = ("[%(asctime)s] [%(levelname)s] %(message)s")

    # Configure and apply console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(console_format_str)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


###############################################################################
# TASKS
###############################################################################


@task
def initialise(ctx):
    """
    Pre-task for checking prerequisites
    """

    global logger

    logger = configure_root_logger()

    try:
        # Check we are running as root
        if os.geteuid() != 0:
            raise Exception("Script must be run as root")
    except Exception as ex:
        logger.critical(str(ex))
        sys.exit(1)


@task(pre=[initialise])
def install_prerequisites(ctx):
    """
    ???
    """
    raise NotImplementedError("install_prerequisites() is not yet implemented")


@task(pre=[initialise])
def run_test(ctx):
    """
    ???
    """

    DEVICE_IDENT = "MTFDKCC15T3TFR"
    SPEC = "enterprise"
    NUM_TO_TEST = 2
    TESTS = [
        "iops",
        "latency",
        "throughput",
    ]

    # --threads_per_core_max=1
    # --timeout=(2 * 86400)

    # Get devices to be tested
    logger.info("Getting devices under test...")
    result = ctx.run(f"nvme list | grep {DEVICE_IDENT}", hide=True)
    block_devs = []
    for line in str(result.stdout).split('\n'):
        line = line.strip()
        block_dev = line.split()[0]
        block_devs.append(block_dev)
    block_devs.sort()

    for i in range(0, NUM_TO_TEST):
        block_dev = block_devs[i]
        logger.info(f"Running tests for '{block_dev}' ...")

        # TODO: Update paths in parameters.json
        # 1) /home/rd41/Desktop/SSS-PTS-TEST/test/ -> unique directory for test
        # 2) /home/rd41/Desktop/SSS-PTS-TEST/report/ -> unique directory for report

    '''
    result = ctx.run(
        f"cat {APT_SOURCES_FILE} | grep '{line}'",
        hide=True,
        warn=True
        )
    if result.exited == 0:
        continue
    '''

    pass


###############################################################################
# END OF TASKS
###############################################################################

# End of script
