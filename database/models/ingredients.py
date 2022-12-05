""" Dataclass model for ingredients """
from dataclasses import dataclass


@dataclass
class Ingredients:
    """Ingredients Model"""

    meat: list = None
    dairy: list = None
    seasoning: list = None
    produce: list = None
    misc: list = None

    def __getitem__(self, key):
        """get attribute"""
        return getattr(self, key)

    def __setitem__(self, key, value):
        """set attribute"""
        return setattr(self, key, value)
