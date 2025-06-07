from .libraryitem import LibraryItem

class Magazine(LibraryItem):
    """
    Represents a magazine in the library management system.
    
    This class is a subclass from LibraryItem, providing specific functionality 
    for magazine items including display item information.
    
    Attributes:
        __type (str): Type of the instances will create using this constructor default 'Magazine'
        
    Methods:
        display_info: Displays all the magazine information (override the abstractmethod)
        dict_to_instance: `Class method` to create a Magazine instance from a dictionary after load items from JSON as dict
        instance_to_dict: Converts the magazine object to a `dictionary` to store it inside the items JSON File
    """
    def __init__(self, title, author, available):
        """
        Initialize a new Magazine instance.
        
        Args:
            title (str): The title of the magazine
            author (str): The author of the magazine
            available (bool): The availability status of the magazine
        """
        super().__init__(title, author, available)
        self.__type = 'Magazine'

    @classmethod
    def dict_to_instance(cls, magazine_dict):
        """
        Convert the magazine item from dictionary to a real instance after load it from the file

        to access the magazine item methods using the instance itself

        Args:
            magazine_dict (dict): All the magazine item information in a dictionary

        Returns:
            Magazine: Returns an instance from the Magazine class
        """
        magazine = cls(magazine_dict['title'], magazine_dict['author'], magazine_dict.get('available', True))
        magazine._LibraryItem__item_id = magazine_dict['item_id'] # to prevent name-mangling (in python)
        magazine.__type = magazine_dict['type']
        return magazine

    # implement the abstract method
    def display_info(self, users):
        """
        Display information about the magazine including its status and borrowed by or reserved by if exist.

        Args:
            users (list): List of User objects to check for borrowed status

        Returns:
            str: Formatted string of magazine information
        """
        borrowed_by_name = None
        # Check the borrowed status
        for user in users:
            user_borrowed_items = user.get_borrowed_items()
            # loop over each item in the user borrowed list
            for item in user_borrowed_items:
                # if this item exist there so store the user name here `borrowed_by_name`
                if self.get_item_id() == item['item_id']:
                    borrowed_by_name = user.get_name()

        # initial value
        item_status = "available ✅" if self.check_availability() else "not available ❌"
        # if borrowed_by_name not None => add it to `item_status` str
        if borrowed_by_name:
            item_status = item_status + f", borrowed by {borrowed_by_name}"    
        
        # then return the result
        return f"\n📝 Magazine: {self.get_title()}\n👲 Author By: {self.get_author()}\n🌍 Status: {item_status}\n🆔 Item ID: {self.get_display_id()}"

    def instance_to_dict(self):
        """Returns the item data as dictionary to store it in the JSON ITems file"""
        return {
            'title': self.get_title(),
            'author': self.get_author(),
            'item_id': self.get_item_id(),
            'type': self.__type,
            'available': self.check_availability()
        }

    def get_type(self):
        """Returns the type of the item"""
        return self.__type