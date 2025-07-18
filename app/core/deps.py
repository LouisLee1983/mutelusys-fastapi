# -*- coding: utf-8 -*-
"""
Dependencies module - alias for dependencies.py for backward compatibility
"""

# Re-export everything from dependencies module
from .dependencies import *
from app.db.session import get_db

# Common dependencies for FastAPI endpoints
__all__ = [
    "get_db",
    "get_current_user", 
    "oauth2_scheme"
]