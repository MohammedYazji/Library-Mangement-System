from .libraryitem import LibraryItem
from .reservable import Reservable

class Book(LibraryItem, Reservable):
    """
    Represents a book in the library management system.
    
    This class is a subclass from 
        - LibraryItem
        - Reservable interface,
    providing specific functionality for book items including display item information
    and make reservation.
    
    Attributes:
        __type (str): Type of the instances will create using this constructor default 'Book'
        
    Methods:
        display_info: Displays all the book information (override the abstractmethod)
        reserve: Reserves a book for a specific user
        cancel_reserve: Cancel an existing reservation
        dict_to_instance: `Class method` to create a Book instance from a dictionary after load items from JSON as dict
        instance_to_dict: Converts the book object to a `dictionary` to store it inside the items JSON File
    """
    def __init__(self, title, author, available):
        """
        Initialize a new Book instance.
        
        Args:
            title (str): The title of the Book
            author (str): The author of the Book
            available (bool): The availability status of the Book
        """
        # Explicitly call to the two constructors
        LibraryItem.__init__(self, title, author, available)
        Reservable.__init__(self)       
        self.__type = 'Book'

    @classmethod
    def dict_to_instance(cls, book_dict):
        """
        Convert the book item from dictionary to a real instance after load it from the file

        to access the item methods using the instance itself

        Args:
            book_dict (dict): all the book item information in a dictionary

        Returns:
            Book: Returns an instance from the Book class
        """
        book = cls(book_dict['title'], book_dict['author'], book_dict.get('available', True))
        book._LibraryItem__item_id = book_dict['item_id'] # to prevent name-mangling (in python)
        book.__type = book_dict['type']
        book._reserved_by = book_dict.get('reserved_by', None)  # Use get() with default None
        return book
    
    # implement the abstract method
    def display_info(self, users):
        """
        Display information about the book including its status, and borrowed by or reserved by if exist.

        Args:
            users (list): List of User objects to check for borrowed and reserved status

        Returns:
            str: Formatted string of DVD information
        """
        borrowed_by_name = None
        reserved_by_name = None
        
        # check the borrowed status
        for user in users:
            user_borrowed_items = user.get_borrowed_items()
            # loop over each item in the user borrowed list
            for item in user_borrowed_items:
                # if this item exist there so store the user name here `borrowed_by_name`
                if self.get_item_id() == item['item_id']:
                    borrowed_by_name = user.get_name()
            
            # check the reserved status
            # if the uer id matches this item id store the user as reserved here `reserved_by_name`
            if user.get_user_id() == self._reserved_by:
                reserved_by_name = user.get_name()
            
        # intial value 
        item_status = "available ✅" if self.check_availability() else "not available ❌"
        # if borrowed_by_name not None => add it to `item_status` str
        if borrowed_by_name:
            item_status = item_status +  f", borrowed by {borrowed_by_name}"
        # if reserved_by_name not None => add it to `item_status` str
        if reserved_by_name:
            item_status = item_status + f", reserved by {reserved_by_name}"            

        # then return the result
        return f"\n📚 Book: {self.get_title()}\n👲 Author By: {self.get_author()}\n🌍 Status: {item_status}\n🆔 Item ID: {self.get_display_id()}"

    # implement the interface methods reserve, cancel_reserve
    # abstract method => must override it
    def reserve(self, user):
        """
        Reserve a book for a specific user.

        Args:
            user (User): The user who wants to reserve the book

        Returns:
            bool: True if reservation was successful, otherwise return false
        """
        # if available and not reserved
        if self.check_availability() and self._reserved_by is None:
            # set the reserved_by value with the ueser id
            self._reserved_by = user.get_user_id()
            # and append the reserved item in the user reserved_item_list
            user.append_reserved_item({'title': self.get_title(), 'author': self.get_author(), 'item_id': self.get_item_id()})
            # set the availability false
            self.set_available(False)
            return True
        else:
            return False
        
    def cancel_reserve(self, user):
        """
        Cancel an existing reservation for the Book

        Args:
            user (User): The user who wants to cancel their reservation

        Returns:
            bool: true if the process success , otherwise return false
        """
        # if the reserved by value is the same as the user id 
        if self.get_reserved_by() == user.get_user_id():
            # reset the reserved_by as None
            self.set_reserved_by(None)
            # reset the availability as true
            self.set_available(True)
            # remove it from the user reserved_item_list
            user.remove_reserved_item({'title': self.get_title(), 'author': self.get_author(), 'item_id': self.get_item_id()})
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