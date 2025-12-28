"""Pocket Flow Playground package."""

import toml as Toml

__app_name__ = "pyproject.toml"
__version__ = Toml.load("pyproject.toml")["project"]["version"]
