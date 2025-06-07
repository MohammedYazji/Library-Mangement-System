import uuid

class User:
    """
        Represents a user class in the application.

        A user can have unique id, email, name, and
        the list of the borrowed items
        """
    def __init__(self, name, email):
        """
        Initialize a new User instance.
        
        Args:
            name (str): the name of the user
            email (str): email of the user should be unique
        """
        self.__user_id = str(uuid.uuid4())
        self.__name = name
        self.__email = email
        self.__borrowed_items = []
        self.__reserved_items = []
    
    @classmethod
    def dict_to_instance(cls, user_dict):
        """
        Convert the user from dictionary to a real instance after load it from the file

        to access the User methods using the instance itself

        Args:
            user_dict (dict): all the user information in a dictionary

        Returns:
            User: Returns an instance from the User class
        """
        user = cls(user_dict['name'],user_dict['email'])
        user.__user_id = user_dict['user_id']
        user.__borrowed_items = user_dict['borrowed_items']
        user.__reserved_items = user_dict['reserved_items']
        return user
    
    def instance_to_dict(self):
        """Convert the User object to a dictionary to 
        append it to the users_data list easily"""
        return {
        "user_id": str(self.__user_id),
        "name": self.__name,
        "email": self.__email,
        "borrowed_items": self.__borrowed_items,
        "reserved_items": self.__reserved_items
    }

    # Getters
    def get_display_id(self):
        """
        Getter to get a short version of the id

        the user id will still the same but I want to let the user dealing with simplify id from just 8 characters

        Returns:
            str: short version from the user id (Just the first 8 characters)
        """
        return self.__user_id[0:8]
    
    def get_user_id(self):
        """Returns the user id"""
        return self.__user_id
    
    def get_borrowed_items(self):
        """Returns the user borrowed list of items"""
        return self.__borrowed_items
    
    def get_reserved_items(self):
        """Returns the user list of reserved items"""
        return self.__reserved_items
    
    def get_name(self):
        """Returns the user name"""
        return self.__name
    
    def get_email(self):
        """Returens the user email"""
        return self.__email
    
    # setters
    def append_borrowed_item(self, item):
        """Add a new item to the user borrowed items list"""
        self.__borrowed_items.append(item)

    def remove_borrowed_item(self, item):
        """Removing an existing item from the user borrowed items list"""
        self.__borrowed_items.remove(item)

    def append_reserved_item(self, item):
        """Add a new item to the user list of reserved items"""
        self.__reserved_items.append(item)

    def remove_reserved_item(self, item):
        """Removing an existing item from the user list of reserved items"""
        self.__reserved_items.remove(item)
