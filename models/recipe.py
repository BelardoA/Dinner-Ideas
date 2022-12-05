""" Dataclass model for recipes """

from dataclasses import dataclass, asdict
import datetime
from models.ingredients import Ingredients


@dataclass
class Recipe:
    """Recipe Model"""

    name: str  # Name of the recipe, required attribute
    ingredients: Ingredients = None  # Dictionary of ingredients
    last_cooked: datetime = None  # Last cooked date
    fast_food: bool = False  # Fast food flag

    def __getitem__(self, key):
        """Attr getter"""
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Attr setter"""
        return setattr(self, key, value)

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
