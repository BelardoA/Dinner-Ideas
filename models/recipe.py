from dataclasses import dataclass
import datetime

@dataclass
class Recipe:

    name: str
    ingredients: dict
    last_cooked: datetime = None
    fast_food: bool = False

    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        return setattr(self, key, value)
