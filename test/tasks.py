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
import traceback

from invoke import task
from typing import List
from natsort import natsorted

###############################################################################
# GLOBAL CONSTANTS
###############################################################################

SCRIPT_VERSION = "0.1"

'''
SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_DIR = SCRIPT_PATH.parent
'''

drive_models = {
    "micron_7450_pro_u3": "MTFDKCC15T3TFR",
}

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


def get_drives_by_ident(ctx, model: str) -> List[str]:
    """
    Returns list of drive block device paths, for devices matching supplied
    model ident
    """
    # Get devices matching ident
    result = ctx.run(f"nvme list | grep {model}", hide=True)
    # Build list of associated block devices
    block_devs = []
    for line in str(result.stdout).split('\n'):
        line = line.strip()
        if len(line) > 0:
            block_dev = line.split()[0]
            block_devs.append(block_dev)

    return natsorted(block_devs)


def block_device_to_char(dev_path: str) -> str:
    """
    Get character device path from drive's block path
    """
    if dev_path[-2] == 'n':
        # Path is that of a block device, so convert to character
        return dev_path[:-2]
    else:
        # Path is already a character device
        return dev_path


def drive_mounted(ctx, drive_path: str) -> bool:
    """
    Returns True if supplied drive is mounted
    """
    result = ctx.run(f"mount | grep {drive_path}", hide=True, warn=True)
    return (result.exited == 0)


def format_drive(ctx, drive_path: str, secure=False):
    """
    Formats drive at supplied path
    """

    # Erase all namespaces without warning
    cmd = (
        f"nvme format {block_device_to_char(drive_path)} "
        "-n 0xffffffff --force"
    )

    # Append arguments for crypto erase, if requested
    if secure:
        # NOTE: Method from https://www.ibm.com/docs/en/linux-on-systems?topic=devices-secure-data-deletion-nvme-drive
        # Check drive support for crypto-erase operation
        result = ctx.run(
            f"nvme id-ctrl {drive_path} | grep fna",
            hide=True,
            warn=True
        )
        if result.stdout.split()[-1] == "0x4":
            logger.debug("Device supports crypto erase")
            erase_mode = 2
        else:
            logger.debug(
                "Device does NOT support crypto erase, "
                "falling back to user data erase"
            )
            erase_mode = 1
        cmd += f" -s={erase_mode}"

    logger.debug(f"cmd='{cmd}'")

    # Perform the erase
    result = ctx.run(cmd, hide=True)
    if "Success formatting namespace" not in result.stdout:
        raise Exception(f"Failed to format drive {drive_path}")


###############################################################################
# TASKS
###############################################################################


@task
def initialise(ctx):
    """
    Pre-task for checking prerequisites
    """

    global logger

    logger = configure_root_logger(debug=True)

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
def setup_raid(ctx):
    """
    ???
    """

    try:
        # Get lists of drives to be included in pool
        drives = get_drives_by_ident(ctx, drive_models["micron_7450_pro_u3"])
        logger.debug(f"drives={drives}")
        logger.debug(f"len(drives)={len(drives)}")
        # Ensure none of the drives are mounted
        for drive in drives:
            if drive_mounted(ctx, drive):
                raise Exception(f"Drive {drive} is mounted - unable to format")
        # Format each drive
        for i in range(0, len(drives)):
            drive = drives[i]
            logger.info(f"Formatting {drive} ({i+1}/{len(drives)}) ...")
            format_drive(ctx, drive)
    except Exception as ex:
        logger.critical(str(ex))
        logger.debug(f"\n{traceback.format_exc()}")
        sys.exit(1)


@task(pre=[initialise])
def run_test(ctx):
    """
    ???
    """

    SPEC = "enterprise"
    NUM_TO_TEST = 2
    TESTS = [
        "iops",
        "latency",
        "throughput",
    ]

    # --threads_per_core_max=1
    # --timeout=(2 * 86400)

    block_devs = get_drives_by_ident(ctx, drive_models["micron_7450_pro_u3"])

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
