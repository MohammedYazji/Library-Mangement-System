from abc import ABC, abstractmethod
import uuid

class LibraryItem(ABC):
    """
    Abstract class representing any item in the library management system.
    
    including book, magazine, and DVD, make common functions for them ,
    but each subclass must to implement display_info in his way (@abstractmethod).
    
    Attributes:
        __item_id (str): Unique id for each item using uuid4
        __title (str): The name of the item
        __author (str): The author of the item
        __available (bool): The availability status of the item
        
    Methods:
        display_info: `Abstract method` to display the item information
        check_availability: check if the item is available, return bool (true, false)
        set_available: Setter method for availability status
    """
    def __init__(self, title, author, available):
        """
        LibraryItem constructor to intializing items objects
        via it's subclasses

        Can't make any instance immediatly from here
        just from the subclasses

        Args:
            title (str): The name of the item
            author (str): the author of the item
            available (bool): the availability status of the item
        """
        self.__item_id = str(uuid.uuid4())
        self.__title = title
        self.__author = author
        self.__available = available

    @abstractmethod
    def display_info(self, users):
        """
        I made this as an abstract method => To enforce the subclasses to override it
        Each subclass (Book, DVD, Magazine) needs to display information in different way
        """
        pass

    def check_availability(self):
        """
        This is normal function not abstract because I don't need to override it
        all subclasses will have the same functionality

        Returns:
            bool: Returns the availability status of the item
        """
        # returns the status using ternary if
        return self.__available if self.__available is not None else True
    
    # Getters [To Deal with the private attributes]
    def get_title(self):
        """Returns the item title"""
        return self.__title
    
    def get_author(self):
        """Returns the item author"""
        return self.__author
    
    def get_item_id(self):
        """Returns the full item id"""
        return self.__item_id
    
    def get_display_id(self):
        """Returns the display item id (just the first 8 characters)"""
        return self.__item_id[0:8]

    # setters [To set private attributes]
    def set_available(self, value):
        """set the availability status of the item"""
        self.__available = value