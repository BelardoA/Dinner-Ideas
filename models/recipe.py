""" Dataclass model for recipes """

from dataclasses import dataclass
import datetime
from models.ingredients import Ingredients


@dataclass
class Recipe:
    """Recipe Model"""

    name: str  # Name of the recipe
    ingredients: Ingredients  # Dictionary of ingredients
    last_cooked: datetime = None  # Last cooked date, defaults to never cooked
    fast_food: bool = False  # Fast food flag, defaults to False

    def __getitem__(self, key):
        """Attr getter"""
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Attr setter"""
        return setattr(self, key, value)
