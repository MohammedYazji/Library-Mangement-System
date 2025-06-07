"""
This module has all validation methods to ensure
the input from users will be correctly, and don't crash the application.
"""
import re
from Exceptions.exceptions import InputNotInRangeError, EmailIsNotValid, EmailAlreadyExistsError, InputFieldEmptyError, UserNotFoundError, ItemNotFoundError, AdminPasswordWrongError, TypeIsNotValidError

# validate input is an integer and in a specifc range
# using to receive choices or inputs from the user
def int_validation(num, start, end, num_type):
    """
    validate if the input from the user is a valid integer in belongs to spedific range,
    or can convert it to an integer

    validation happens through except [valueError or my custom Error 'InputNotInRangeError']

    Args:
        num (str): Receives a string from the user through `input()` method
        start (int): the start of the range should the number be inside it
        end (int): the end of the range should the number be inside it
        num_type (str): Recive a string which is the number type which will receive for example is it a `choice` 

    Raises:
        InputNotInRangeError: Raises an exception if the number not in the range of choices

    Returns:
        int : Returns the input if it's a valid integer 
    """
    # While true keep receive inouts until return the right value
    while True:
        try:
            # try to convert the value to integer
            value = int(num) # maybe will cause valueError

            if not (start <= value <= end): 
                # custom InputNotInRangeError
                raise InputNotInRangeError(f"\n👎 {num_type.capitalize()} must be between {start} - {end}")
            
            return value
        
        except ValueError:
            num = input(f"\n👎 {num_type} can't be a string, Please enter a valid {num_type} (Just numbers allow): ")

        except InputNotInRangeError as e:
            print(e)
            num = input(f'Please enter a valid {num_type} (between {start} - {end}): ')

# validate the email (I use Stack overflow to learn about email validations process, and regax)
def email_validation(email, users):
    """
    Validate the email

    Validate that if the email formatting is valid according to this regax,
    and at the same time that the email dosen't exist before.

    Args:
        email (str): receive the email as a string to validate it
        users (list): list of all users information as instances

    Raises:
        InputFieldEmptyError: Raises an error if the email is empty
        EmailIsNotValid: Raises an error if the email formatting is not valid.
        EmailAlreadyExistsError: Raises an error if the email is already linked with another user.

    Returns:
        str: Return the email after pass validation process
    """
    while True:
        try:
            # First check if email is empty
            if not email:
                raise InputFieldEmptyError("\n❌ You can't left the email empty!")

            # check if the email is valid using regax
            valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

            # if not valid raise a custom error => `EmailIsNotValid`
            if not valid:
                raise EmailIsNotValid('\n❌ Email Formmating is not valid...')
            
            # check if the email is already exist with another user if yes raise a custom exception => `EmailAlreadyExistsError`
            for user in users:
                user_email = user.get_email().lower()
                if email == user_email:
                    raise EmailAlreadyExistsError("\n❌ This email already linked with another user")
                
            # else if the email is valid return it.
            return email

        except InputFieldEmptyError as e:
            print(e)
            email = input('Please enter the email: ').lower()

        except EmailIsNotValid as e:
            print(e)
            email = input('Please enter a valid email (e.g, example@gmail.com): ').lower()

        except EmailAlreadyExistsError as e:
            print(e)
            email = input('Please try again with another email: ').lower()

# check if the input field field is empty
def empty_input_validation(name, message):
    """
    check if the user input an empty string

    Args:
        name (str): Receive input from the user to validate it
        message (str): the type of the input (e.g, title, name, author)

    Raises:
        InputFieldEmptyError: Rasies error when the user left the name empty

    Returns:
        str: Retuens the string after validation it's not empty
    """
    while True:
        try:
            # check if the input is empty
            if not name:
                raise InputFieldEmptyError(f"\n❌ You can't left the {message} empty!")
            
            # else if not empty return it
            return name
            
        except InputFieldEmptyError as e:
            print(e)
            name = input(f"Please input the {message}: ").strip()

# validate the user id => (exist and valid)
def user_id_validation(display_user_id, users):
    """
    Receive the user display id (the first 8 characters from ID) and validate if there's matches value

    Receive the user display id (the first 8 characters from ID),
    then check if the input it's empty => raise custom error `InputFieldEmptyError`,
    and if the length is different from 8 => raise custom error `InputNotInRangeError`,
    then search about the user => if dosen't exist => raise custom error `UserNotFoundError`,
    else return the matched_user.

    Args:
        display_user_id (str): the first 8 characters from the full_user_id
        users (list): list of users

    Raises:
        InputFieldEmptyError: Raise an error if the user dosen;t input any value
        InputNotInRangeError: Raise an error if the user input ID doesn't contains 8 characters
        UserNotFoundError: Raise an error when there's no any matched_user by this ID

    Returns:
        User: Returns the matched user as instance from User class 
    """
    while True:
        try:
            # check if the user didn't input the id value
            if not display_user_id:
                raise InputFieldEmptyError("\n❌ You can't left the id empty!")
            
            # check if the user input ID different from 8 characters
            if  len(display_user_id) != 8:
                raise InputNotInRangeError("\n❌ User id must be 8 characters!")
            
            # searching for the user using the display_user_id
            matched_user = None
            for user in users:
                full_user_id = user.get_user_id()
                # if startswith the same values => so this is the user
                if full_user_id.startswith(display_user_id):
                    matched_user = user
                
            if not matched_user:
                raise UserNotFoundError("\n❌ User dosen't exist...")

            return matched_user

        except InputFieldEmptyError as e:
            print(e)
            display_user_id = input('Please input the user id: ').strip()
        
        except InputNotInRangeError as e:
            print(e)
            display_user_id = input('Please input the user id: ').strip()

        except UserNotFoundError as e:
            print(e)
            break

# validate the item id => (exist and valid)
def item_id_validation(display_item_id, items):
    """
    Receive the item display id (the first 8 characters from ID) and validate if there's matches value

    Receive the item display id (the first 8 characters from ID),
    then check if the input it's empty => raise custom error `InputFieldEmptyError`,
    and if the length is different from 8 => raise custom error `InputNotInRangeError`,
    then search about the item => if dosen't exist => raise custom error `UserNotFoundError`,
    else return the matched_item.

    Args:
        display_user_id (str): the first 8 characters from the full_item_id
        items (list): list of items

    Raises:
        InputFieldEmptyError: Raise an error if the user dosen't input any value
        InputNotInRangeError: Raise an error if the user input ID doesn't contains 8 characters
        UserNotFoundError: Raise an error when there's no any matched_item by this ID

    Returns:
        User: Returns the matched item as instance from Item class 
    """
    while True:
        try:
            # check if the user didn't input the id value
            if not display_item_id:
                raise InputFieldEmptyError("\n❌ You can't left the item id empty!")
            
            # check if the input_id dosen't contains just 8 characters
            if  len(display_item_id) != 8:
                raise InputNotInRangeError("\n❌ Item id must be 8 characters!")
            
            # searching for the item
            matched_item = None
            for item in items:
                # if the full_item_id is startswith the same input display_item_id characters
                # if yes please put this item as the matched_item
                full_item_id = item.get_item_id()
                if full_item_id.startswith(display_item_id):
                    matched_item = item
            
            # raise an error if there'e no item found by this id
            if not matched_item:
                raise ItemNotFoundError("\n❌ Item dosen't exist...")

            return matched_item

        except InputFieldEmptyError as e:
            print(e)
            display_item_id = input('Please input your item id: ').strip()
        
        except InputNotInRangeError as e:
            print(e)
            display_item_id = input('Please input your item id: ').strip()

        except ItemNotFoundError as e:
            print(e)
            break

# check is the admin password is correct
def check_admin(password):
    """
    check if the admin password is correctly
    Args:
        password (str): Receive a password from the user to validate it

    Raises:
        InputFieldEmptyError: Rasies error when the user left the name empty
        AdminPasswordWrongError: Rasies error when the admin password is wrong

    Returns:
        str: Retuens 'admin' if the password is correct, ot
    """
    while True:
        try:
            # check if the password is empty
            if not password:
                raise InputFieldEmptyError("\n❌ You can't left the password empty!")
            
            if password != '12345':
                raise AdminPasswordWrongError("\n❌ Please input the correct password. ")
            
            return 'admin'
            
        except InputFieldEmptyError as e:
            print(e)
            password = input("Please input the admin password: ")
        
        except AdminPasswordWrongError as e:
            print(e)
            password = input('Enter the correct admin password, or -1 to back to the main menu: ')
            if password == '-1':
                return 'stop'
            
# check if the user input a valid item type
def type_validation(item_type):
    """
    check if the user input a valid item type

    Args:
        item_type (str): Receive the type as an input from the user to validate
        is it valid type

    Raises:
        InputFieldEmptyError: Rasies error when the user left the name empty
        TypeIsNotValidError: Rasies error when the user input invalid item type
    Returns:
        str: Retuens the string after validation it's not empty and valid type
    """
    while True:
        try:
            # check if the type is empty
            if not item_type:
                raise InputFieldEmptyError("\n❌ You can't left the item type empty!")
            
            item_type = item_type.strip()
            # Because DVD class is different from others not capitalize not as a title
            # so we need to add additional functionality to consider it correct if input (Dvd, dvd, dVD)
            if item_type.lower() == 'dvd':
                item_type = 'DVD'
            else:
                # otherwise make it a title
                item_type = item_type.capitalize()
            
            # if the input type not one of these types
            if item_type not in ['Book', 'DVD', 'Magazine']:
                raise TypeIsNotValidError('\n❌ Invalid Item Type... ')
            
            return item_type
            
        except InputFieldEmptyError as e:
            print(e)
            item_type = input("Please input the item type: ")

        except TypeIsNotValidError as e:
            print(e)
            item_type = input("\nPlease enter a valid type (Book, DVD, Magazine): ").strip()