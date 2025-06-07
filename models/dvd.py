from .libraryitem import LibraryItem
from .reservable import Reservable

class DVD(LibraryItem, Reservable):
    """
    Represents a DVD in the library management system.
    
    This class is a subclass from 
        - LibraryItem
        - Reservable interface,
    providing specific functionality for DVD items including display item information
    and make reservation.
    
    Attributes:
        __type (str): Type of the instances will create using this constructor default 'DVD'
        
    Methods:
        display_info: Displays all the DVD information (override the abstractmethod)
        reserve: Reserves the DVD for a specific user
        cancel_reserve: Cancels an existing reservation
        dict_to_instance: `Class method` to create a DVD instance from a dictionary after load items from JSON as dict
        instance_to_dict: Converts the DVD object to a `dictionary` to store it inside the items JSON File
    """
    def __init__(self, title, author, available):
        """
        Initialize a new DVD instance.
        
        Args:
            title (str): The title of the DVD
            author (str): The author of the DVD
            available (bool): The availability status of the DVD
        """
        LibraryItem.__init__(self, title, author, available)  # Explicit call to LibraryItem constructor
        Reservable.__init__(self)   
        self.__type = 'DVD'

    @classmethod
    def dict_to_instance(cls, dvd_dict):
        """
        Convert the DVD item from dictionary to a real instance after load it from the file

        to access the DVD item methods using the instance itself

        Args:
            dvd_dict (dict): All the DVD item information in a dictionary

        Returns:
            DVD: Returns an instance from the DVD class
        """
        dvd = cls(dvd_dict['title'], dvd_dict['author'], dvd_dict.get('available', True))
        dvd._LibraryItem__item_id = dvd_dict['item_id']  # to prevent name-mangling (in python)
        dvd.__type = dvd_dict['type']
        dvd._reserved_by = dvd_dict.get('reserved_by', None)  # Use get() with default None
        return dvd

    def display_info(self, users):
        borrowed_by_name = None
        reserved_by_name = None
        
        # Check the borrowed status
        for user in users:
            user_borrowed_items = user.get_borrowed_items()
            # loop over each item in the user borrowed list
            for item in user_borrowed_items:
                # if this item exist there so store the user name here `borrowed_by_name`
                if self.get_item_id() == item['item_id']:
                    borrowed_by_name = user.get_name()
            
            # Check the reserved status
            # if the user id matches this item id store the user as reserved here `reserved_by_name`
            if user.get_user_id() == self._reserved_by:
                reserved_by_name = user.get_name()
        
        # initial value 
        item_status = "available ✅" if self.check_availability() else "not available ❌"
        # if borrowed_by_name not None => add it to `item_status` str
        if borrowed_by_name:
            item_status = item_status + f", borrowed by {borrowed_by_name}"
        # if reserved_by_name not None => add it to `item_status` str
        if reserved_by_name:
            item_status = item_status + f", reserved by {reserved_by_name}"            

        # then return the result
        return f"\n📀 DVD: {self.get_title()}\n👲 Author By: {self.get_author()}\n🌍 Status: {item_status}\n🆔 Item ID: {self.get_display_id()}"

    def reserve(self, user):
        """
        Reserve the DVD for a specific user.

        Args:
            user (User): The user who wants to reserve the DVD

        Returns:
            bool: True if reservation was successful, otherwise False
        """
        if self.check_availability() and self._reserved_by is None:
            self._reserved_by = user.get_user_id()
            user.append_reserved_item({
                'title': self.get_title(), 
                'author': self.get_author(), 
                'item_id': self.get_item_id()
            })
            self.set_available(False)
            return True
        return False
        
    def cancel_reserve(self, user):
        """
        Cancel an existing reservation for the DVD.

        Args:
            user (User): The user who wants to cancel their reservation

        Returns:
            bool: True if cancellation was successful, False otherwise
        """
        if self.get_reserved_by() == user.get_user_id():
            self.set_reserved_by(None)
            self.set_available(True)
            user.remove_reserved_item({
                'title': self.get_title(), 
                'author': self.get_author(), 
                'item_id': self.get_item_id()
            })
            return True
        return False

    # Getters
    def instance_to_dict(self):
        """Returns the item data as dictionary to store it in the JSON ITems file"""
        return {
            'title': self.get_title(),
            'author': self.get_author(),
            'item_id': self.get_item_id(),
            'type': self.__type,
            'reserved_by': self._reserved_by,
            'available': self.check_availability()
        }
    
    def get_type(self):
        """Returns the type of the item"""
        return self.__type
    
    def get_reserved_by(self):
        """Returns the reserved_by value of the item"""
        return self._reserved_by
    
    # Setters
    def set_reserved_by(self, val):
        """set the reserved by value of the item"""
        self._reserved_by = val