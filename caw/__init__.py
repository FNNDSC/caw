from importlib.metadata import Distribution
from packaging import version

__pkg = Distribution.from_name(__package__)

__version__ = version.Version(__pkg.version)
