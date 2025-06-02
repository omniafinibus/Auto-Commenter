# ==================================================================== #
#  File name:      log.py                       #        _.==._        #
#  Author:         Arjan Lemmens                #     .+=##**##=+.     #
#  Date:           18-Jul-2023                  #    *= #        =*    #
#  Company:        Nexperia                     #   #/  #         \#   #
#  Description:    Method used to initialize    #  |#   #   $      #|  #
#                  the global logger.           #  |#   #   #      #|  #
#  Rev:            3.2                          #   #\  #   #     /#   #
#                                               #    *= #   #    =+    #
#                                               #     *++######++*     #
#                                               #        *-==-*        #
# ==================================================================== #

# =========== #
#   Imports   #
# =========== #
# Import logging utilities
import os
import logging
import logging.handlers

# ============================================================== #
#   Methods                                                   #
# ============================================================== #


def setup_custom_logger(
    name: str,
    directory: str = "./",
    makeFolder: bool = False,
    loggingLevel: int = logging.DEBUG,
):
    """
    Initialize a logger with various configuration settings.

    :param name: Name of the logger to setup, use root for global logger
    :type name: string
    :param directory: Directory to write log files to, defaults to "./"
    :type directory: string, optional
    :param makeFolder: Create directory if missing, defaults to False
    :type makeFolder: boolean, optional
    :param loggingLevel: Logging level, defaults to logging.DEBUG
    :type loggingLevel: integer, optional
    :return: Configured logger instance
    :rtype: Logger
    """
    # Log file configuration
    log_file = f"{directory}/commenter.log"
    log_file_max_size = 1024 * 1024 * 20  # Maximum size in megabytes
    log_num_backups = 3  # Number of backups to keep
    log_format = "[%(levelname)s] %(message)s"  # Logging format
    log_filemode = "w"  # Mode for file handling (w: overwrite, a: append)

    # Create the directory if needed and prepare logging handlers
    if not os.path.isdir(directory) and makeFolder:
        os.makedirs(directory)

    # Configure basic logging setup
    logging.basicConfig(
        filename=log_file, format=log_format, filemode=log_filemode, level=loggingLevel
    )

    # Add a rotating file handler for log files
    rotate_file = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=log_file_max_size, backupCount=log_num_backups
    )
    # Configure console output
    consoleHandler = logging.StreamHandler()
    logFormatter = logging.Formatter(log_format)
    consoleHandler.setFormatter(logFormatter)

    # Add both handlers to the logger
    logger = logging.getLogger(name)
    logger.addHandler(rotate_file)
    logger.addHandler(consoleHandler)

    return logger


def change_log_file(loggerName: str, newDir: str, makeFolder: bool = False):
    """
    Change the directory where logging files are written.

    :param name: Name of the logger to setup, use root for global logger
    :type name: string
    :param newDir: New directory to write logs to
    :type newDir: string
    :param makeFolder: Create directory if missing, defaults to False
    :type makeFolder: boolean, optional
    """
    # Ensure the new directory exists before creating logging files
    if not os.path.isdir(newDir) and makeFolder:
        os.makedirs(newDir)

    # Configure log file settings
    log_file_max_size = 1024 * 1024 * 20  # Maximum size in megabytes
    log_num_backups = 3  # Number of backups to keep

    # Prepare and configure the rotating file handler
    rotate_file = logging.handlers.RotatingFileHandler(
        f"{newDir}/commenter.log",
        maxBytes=log_file_max_size,
        backupCount=log_num_backups,
    )

    # Get or create the logger instance
    logger = logging.getLogger(loggerName)
    logger.addHandler(rotate_file)