"""Akor: read-only mission prequalification between sister repositories.

No live mission orchestration or student authorization is implemented here.
"""

__version__ = "0.1.0"

from .preflight import build, review_html, locate

__all__ = ["__version__", "build", "review_html", "locate"]
