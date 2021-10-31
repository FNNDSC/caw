from importlib.metadata import Distribution
from packaging import version

pkg = Distribution.from_name(__package__)

__version__ = version.Version(pkg.version)
