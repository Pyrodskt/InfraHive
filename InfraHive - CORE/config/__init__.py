# db/__init__.py
"""
Package de gestion paramètres de l'application.
Contient :
- Settings : Gestion des settings de l'application
- autres modules config à venir
"""

from .settings import Settings

__all__ = ["Settings"]
