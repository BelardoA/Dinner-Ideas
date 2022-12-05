""" Recipe class """

from dataclasses import dataclass
import datetime


@dataclass
class Recipe:
    """Dataclass for recipe objects"""

    name: str  # Name of the recipe
    ingredients: dict  # Dictionary of ingredients
    last_cooked: datetime = None  # Last cooked date, defaults to never cooked
    fast_food: bool = False  # Fast food flag, defaults to False

    def __getitem__(self, key):
        """Attr getter"""
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Attr setter"""
        return setattr(self, key, value)
