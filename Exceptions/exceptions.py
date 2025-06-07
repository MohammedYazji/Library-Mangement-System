"""
This exceptions module: has many custom exception
I made them to raise errors when something goes wrong
"""
class ItemNotAvailableError(Exception):
    """when the requested item is not available."""
    pass

class UserNotFoundError(Exception):
    """when a user is not found in the database."""
    pass

class ItemNotFoundError(Exception):
    """when an item is not found."""
    pass

class EmailIsNotValid(Exception):
    """when try to register with an email that already exists."""
    pass

class EmailAlreadyExistsError(Exception):
    """when try to register with an email that already exists."""
    pass

class InputFieldEmptyError(Exception):
    """when the input field left empty without any value""" 
    pass

class InputNotInRangeError(Exception):
    """When the number not in a specific range"""
    pass

class FileIsEmptyError(Exception):
    """when JSON File is empty just  empty list without content []"""
    pass

class ItemCanNotReserve(Exception):
    """When User try to reserve a magazine"""
    pass

class AdminPasswordWrongError(Exception):
    """When the admin input wrong password"""
    pass

class TypeIsNotValidError(Exception):
    """When user input unvalid item type"""
    pass