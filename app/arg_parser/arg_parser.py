import argparse
from enum import Enum

from app import config


class Command(str, Enum):
    UPDATE_SST_DATABASE = "createsstdb"
    NO_COMMAND = ""


class ArgParser:

    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(
                prog=config.APP_NAME,
                description=config.APP_DESCRIPTION)
        self._parser.add_argument("command", nargs="?", default="")

    def get_args(self) -> argparse.Namespace:
        return self._parser.parse_args()
