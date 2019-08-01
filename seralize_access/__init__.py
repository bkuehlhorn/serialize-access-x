import pkg_resources
from . import seralize_access  # noqa: F401


__all__ = ["seralize_access"]
__version__ = pkg_resources.get_distribution("seralize-access").version
