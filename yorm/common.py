"""Common exceptions, classes, and functions."""

import os
import shutil
import logging

import yaml

verbosity = 0  # global verbosity setting for controlling string formatting
PRINT_VERBOSITY = 0  # minimum verbosity to using `print`
STR_VERBOSITY = 3  # minimum verbosity to use verbose `__str__`
MAX_VERBOSITY = 4  # maximum verbosity level implemented


def _trace(self, message, *args, **kws):  # pragma: no cover (manual test)
    """Handler for a new TRACE logging level."""
    if self.isEnabledFor(logging.DEBUG - 1):
        self._log(  # pylint: disable=W0212
            logging.DEBUG - 1, message, args, **kws)


logging.addLevelName(logging.DEBUG - 1, "TRACE")
logging.Logger.trace = _trace

logger = logging.getLogger
log = logger(__name__)


# exception classes ##########################################################


# disk helper functions ######################################################


def create_dirname(path):  # pragma: no cover (integration test)
    """Ensure a parent directory exists for a path."""
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.isdir(dirpath):
        log.info("creating directory {}...".format(dirpath))
        os.makedirs(dirpath)


def read_lines(path, encoding='utf-8'):  # pragma: no cover (integration test)
    """Read lines of text from a file.

    :param path: file to write lines
    :param encoding: output file encoding

    :return: path of new file

    """
    log.trace("reading lines from '{}'...".format(path))
    with open(path, 'r', encoding=encoding) as stream:
        for line in stream:
            yield line


def read_text(path, encoding='utf-8'):  # pragma: no cover (integration test)
    """Read text from a file.

    :param path: file path to read from
    :param encoding: input file encoding

    :return: string

    """
    log.trace("reading text from '{}'...".format(path))
    with open(path, 'r', encoding=encoding) as stream:
        text = stream.read()
    return text


def load_yaml(text, path):
    """Parse a dictionary from YAML text.

    :param text: string containing dumped YAML data
    :param path: file path for error messages

    :return: dictionary

    """
    # Load the YAML data
    try:
        data = yaml.load(text) or {}
    except yaml.error.YAMLError as exc:
        msg = "invalid contents: {}:\n{}".format(path, exc)
        raise ValueError(msg) from None
    # Ensure data is a dictionary
    if not isinstance(data, dict):
        msg = "invalid contents: {}".format(path)
        raise ValueError(msg)
    # Return the parsed data
    return data


def write_lines(lines, path, end='\n', encoding='utf-8'):  # pragma: no cover (integration test)
    """Write lines of text to a file.

    :param lines: iterator of strings
    :param path: file to write lines
    :param end: string to end lines
    :param encoding: output file encoding

    :return: path of new file

    """
    log.trace("writing lines to '{}'...".format(path))
    with open(path, 'wb') as stream:
        for line in lines:
            data = (line + end).encode(encoding)
            stream.write(data)
    return path


def write_text(text, path, encoding='utf-8'):  # pragma: no cover (integration test)
    """Write text to a file.

    :param text: string
    :param path: file to write text
    :param encoding: output file encoding

    :return: path of new file

    """
    if text:
        log.trace("writing text to '{}'...".format(path))
    with open(path, 'wb') as stream:
        data = text.encode(encoding)
        stream.write(data)
    return path


def touch(path):  # pragma: no cover (integration test)
    """Ensure a file exists."""
    if not os.path.exists(path):
        log.trace("creating empty '{}'...".format(path))
        write_text('', path)


def delete(path):  # pragma: no cover (integration test)
    """Delete a file or directory with error handling."""
    if os.path.isdir(path):
        try:
            log.trace("deleting '{}'...".format(path))
            shutil.rmtree(path)
        except IOError:
            # bug: http://code.activestate.com/lists/python-list/159050
            msg = "unable to delete: {}".format(path)
            log.warning(msg)
    elif os.path.isfile(path):
        log.trace("deleting '{}'...".format(path))
        os.remove(path)