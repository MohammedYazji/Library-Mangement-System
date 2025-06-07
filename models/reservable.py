from abc import ABC, abstractmethod

class Reservable(ABC):
    """
    `Abstract interface` for items that can reserved by users
    (just the book, and dvd.)

    Book, and DVD classes must Reimplement reserve and cancel_reserve methods.
    
    Attributes:
        _reserved_by (str): ID of the user who reserved this item, or None
            I make it protected not private due to name mangling
        
    Methods:
        reserve: `Abstract method` to reserve the item for a user
        cancel_reserve: `Abstract method` to cancel a reservation
    """

    def __init__(self):
        """
        Each Book, or DVD item will has _reserved_by attributes by default None
        """
        self._reserved_by = None # here private casued an issue

    @abstractmethod
    def reserve(self, user):
        """must implement it in the subclasses Book, DVD"""
        pass

    @abstractmethod
    def cancel_reserve(self, user):
        """must implement it in the subclasses Book, DVD"""
        pass

