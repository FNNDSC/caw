from importlib.metadata import Distribution

pkg = Distribution.from_name(__package__)

__version__ = pkg.version
