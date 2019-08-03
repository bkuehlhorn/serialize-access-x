import pkg_resources
from . import serialize_access  # noqa: F401


__all__ = ["serialize_access"]
__version__ = pkg_resources.get_distribution("serialize_access").version
