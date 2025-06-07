from services import storage

class Library:
    """
    Class representing the library management in the library management system.
    
    Attributes:
        __users (str): The list of all users instances
        __items (str): The list of all items instances
        
    Methods:
        display_info: `Abstract method` to display the item information
        check_availability: check if the item is available, return bool (true, false)
        set_available: Setter method for availability status
    """
    def __init__(self, users, items):
        """
        Library constructor to intializing a new Library
        Instancce

        Args:
            users (list): The list of all users instances
            items (list): The list of all items instances
        """
        self.__users = users
        self.__items = items

    # Getters
    def get_users(self):
        """Returns the list of users instances"""
        return self.__users
    
    def get_items(self):
        """Returns the list of items instances"""
        return self.__items

    #  Adding an item
    def add_item(self, item):
        """Add a new item for the items list"""
        self.__items.append(item)

    # Removing an item from the items list
    def remove_item(self, item):
        """Removing an existing item from the items list"""
        if item in self.__items:
            self.__items.remove(item)
            return True 
        else:
            return False

    #  Adding user
    def add_user(self, user):
        """Add a new User to the users list"""
        self.__users.append(user)
        return True

    #  Removing user
    def remove_user(self, user):
        """Remove an existing user from the users list"""
        if user in self.__users:
            self.__users.remove(user)
            return True
        else:
            return False

    #  Borrowing an item
    def borrow_item(self, user, item):
        """Borrowing an item if it's available"""
        # Check if item is available and not already borrowed by this user
        if not item.check_availability():
            return False
            
        # Check if user already has this item borrowed
        for borrowed_item in user.get_borrowed_items():
            if borrowed_item['title'] == item.get_title():
                return False
                
        # If we get here, item is available and user doesn't have it
        item.set_available(False)
        user.append_borrowed_item({
            'title': item.get_title(), 
            'author': item.get_author(),
            'item_id': item.get_item_id()
        })
        return True

    #  Returning an item
    def return_item(self, user, item):
        """Returning an item if it's already in the user borrowed_items list"""
        for i in user.get_borrowed_items():
            if i['title'] == item.get_title():
            # make it available again
                item.set_available(True)
                user.remove_borrowed_item({
                    'title': item.get_title(),
                    'author': item.get_author(),
                    'item_id': item.get_item_id()        
            })
                return True
        else:
            return False

    #  Reserving items using the reserve function from Reservable interface
    def make_reservation(self, user, item):
        """Reserve an item for a specific user"""
        if item.reserve(user):
            return True
        else:
            return False
        
    #  Cancel reservation using cancel_reserve function from Reservable interface
    def cancel_reserve(self, user, item):
        """Cancel the reservation for a specific item"""
        if item.cancel_reserve(user):
            return True
        else:
            return False

