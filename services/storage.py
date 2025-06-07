"""
This storage module: will dealing with the files 
load, search, or even save data from and to the JSON FILES
"""
import os
import json
from models.user import User
from models.book import Book
from models.magazine import Magazine
from models.dvd import DVD
from Exceptions.exceptions import FileIsEmptyError, UserNotFoundError, ItemNotFoundError
from . import display

# USE CONSTANTS (THE FILES NAMES)
ITEMS_FILE_NAME = 'data/items.json'
USERS_FILE_NAME = 'data/users.json'

# load all items from the JSON File
def load_items():
    """
    This Method will load all items data from the JSON File

    Receive the items from the json file as JS-Objects , Python-dictionaries
    and convert them back into Item instances using `classmethod` `to_dict()` to let us use the item methods

    Returns:
        list : Returns a list contains all items instances
    """
    try:
        # if the file doesn't exist make one with []
        if not os.path.exists(ITEMS_FILE_NAME):
            # if the file doesn't Exist IOError
            raise IOError("\n❌ Warning: Items File Dosen't Exist...")
        
        with open(ITEMS_FILE_NAME, 'r') as f:
            items = []
            items_data = json.load(f)
            if not items_data:  # Check if file is empty
                raise FileIsEmptyError("\n❌ Warning: Items file is empty...")

            # loop over items dictionaries and convert them back into
            # instances using `dict_to_instance` `@classmethod` why!? => to use the item methods
            for item in items_data:
                item_type = item['type']

                if item_type == 'Book':
                    items.append(Book.dict_to_instance(item))
                elif item_type == 'Magazine':
                    items.append(Magazine.dict_to_instance(item))
                elif item_type == 'DVD':
                    items.append(DVD.dict_to_instance(item))

            # return the list of items instances
            return items

    except IOError as e:
        print(e)
        return []
    
    except FileIsEmptyError as e:
        print(e)
        return []
    
    except json.decoder.JSONDecodeError as e:
        print('\n❌ Items file is not formatted correctly')
        return []

    except Exception:
        print("\n❌ Failed to read items file...")
        return []

# load all users from the JSON File
def load_users():
    """
    This Method will load all users data from the JSON File

    Receive the users from the json file as JS-Objects => Python-dictionaries
    and convert them back into User instances using `classmethod` `to_dict()` to let us use the user methods

    Returns:
        list : Returns a list contains all users instances
    """
    try:
        # if the file doesn't Exist IOError
        if not os.path.exists(USERS_FILE_NAME):
            raise IOError("\n❌ Warning: Users File Dosen't Exist...")

        with open(USERS_FILE_NAME, 'r') as f:
            users = []
            users_data = json.load(f)
            if not users_data:
                raise FileIsEmptyError("\n❌ Warning: Users file is empty...")

            # loop over users dictionaries and convert them back into
            # instances using `dict_to_instance()` `@classmethod` why!? => to use the user methods
            for user in users_data:
                user = User.dict_to_instance(user)
                users.append(user)

            # return the list of items instances
            return users
    
    except IOError as e:
        print(e)
        return []
    
    except FileIsEmptyError as e:
        print(e)
        return []
    
    except json.decoder.JSONDecodeError as e:
        print('\n❌ Users file is not formatted correctly')
        return []

    except Exception:
        print("\n❌ Failed to read users file...")
        return []

# Search for items based on title
def search_by_title(search_query, items, users):
    """
    Get the items that has the same title as given

    Receive a search_query => the title to search about, and items list => to search on it about similar results,
    then add the matchs items to search_result list to display it later using `display_search_result()` function

    Args:
        search_query (str): The title to search based on it
        items (list): list of all items
        users (list): list of all users
    """
    search_result = []

    # loop over items and add the matches items to the search_result
    # I used `startswith()` not == to can found more results
    for item in items:
        item_title = item.get_title().lower()
        # if user enter just the start of the title will works
        if item_title.startswith(search_query):
            search_result.append(item)
        
        # and if enter any word inside the title also will work
        elif len(search_query) > 2 and search_query in item_title:
            search_result.append(item)
        
    # display the search result
    display.display_search_result(search_query, search_result, users)

# Search for items based on type
def search_by_type(search_query, items, users):
    """
    Get the items that has the same type as given

    Receive a search_query => the type to search about, and items list => to search on it about similar results,
    then add the matchs items to search_result list to display it later using `display_search_result()` function

    Args:
        search_query (str): The type to search based on it
        items (list): list of all items
        users (list): list of all users

    """
    search_result = []
    
    # loop over items_data and add the matches items to the search_result
    for item in items:
        item_type = item.get_type().lower()
        if item_type == search_query:
            search_result.append(item)

    # display the search result
    display.display_search_result(search_query, search_result, users)

# Stores the users list after updating it
def store_users(updated_users_list):
    """
    stores the updating users list into the JSON file

    Rewrite the usere file and put inside it the users as dictionaries again,
    after convert the users instances into dictionaries
    using `instance_to_dict()` user method

    Args:
        updated_users_data (list): The updating list of useers to store it

    Returns:
        bool: Returns true if the process done, otherwise False
    """
    try:
        # make a list to store instances after convert them
        users = []

        # loop over the updated users list and convert them
        # each user instance to a dictionary contains it's information
        for user in updated_users_list:
            user_dict = user.instance_to_dict()
            users.append(user_dict)

        if not os.path.exists(USERS_FILE_NAME):
            # if the file doesn't Exist IOError
            raise IOError("\n❌ Warning: Users File Dosen't Exist...")
        
        # save the users list of dictionaries
        # indent=4 to write the objects in the JSON file in nice formatting
        with open(USERS_FILE_NAME, 'w') as f:
            json.dump(users, f, indent=4)
            return True

    except IOError as e:
        print(e)
        return False
    
    except json.decoder.JSONDecodeError:
        print('\n❌ Users file is not formatted correctly')
        return False

    except Exception:
        print("\n❌ Failed to save users file...")
        return False

# Stores the items list after updating it
def store_items(updated_items_list):
    """
    stores the updating items list into the JSON file

    Rewrite the items file and put inside it the items as dictionaries again,
    after convert the items instances into dictionaries
    using `instance_to_dict()` item method

    Args:
        updated_items_data (list): The updating list of items

    Returns:
        bool: Returns true if the process done, otherwise false
    """
    try:
        # make a list to store instances after convert them
        items = []

        # loop over the updated items list and convert
        # each item instance to a dictionary contains it's information
        for item in updated_items_list:
            item_dict = item.instance_to_dict()
            items.append(item_dict)

        if not os.path.exists(ITEMS_FILE_NAME):
                # if the file doesn't Exist IOError
                raise IOError("\n❌ Warning: Items File Dosen't Exist...")
        
        # save the items list of dictionaries
        with open(ITEMS_FILE_NAME, 'w') as f:
            json.dump(items, f, indent=4)
            return True

    except IOError as e:
        print(e)
        return False
    
    except json.decoder.JSONDecodeError:
        print('\n❌ Items file is not formatted correctly')
        return False

    except Exception:
        print("\n❌ Failed to save items file...")
        return False

# update a user value
def update_users(users, user):
    """
    Updates a user in the users list and save it to the users file

    to ensure all data will keep sync

    Args:
        users (list): List of all users
        user (User): User to update

    Returns:
        bool: true if update successful, otherwise false
    """
    try:
        # first we need to find the user in the list
        user_found = False
        # looping over users using enumerate to access the index and the value for each user
        for index, u in enumerate(users):
            # if the user has the same id with the user i want to update
            if u.get_user_id() == user.get_user_id():
                # update the user by reassign the new value
                users[index] = user
                user_found = True
                break

        # if we didn't find the user, raise an error
        if not user_found:
            raise UserNotFoundError(f"User {user.get_name()} not found in users list")

        # try to save the changes to the file
        if not store_users(users):
            raise IOError("Failed to save user changes to file")

        return True

    except UserNotFoundError as e:
        print(e)
        return False

    except Exception:
        print("❌ Failed to update user...")
        return False

# update an item value
def update_items(items, item):
    """
    Updates an item in the items list and saves it to the items file

    Args:
        items (list): List of all items
        item (LibraryItem): Item to update

    Returns:
        bool: True if update successful, False otherwise
    """
    try:
        # find the item in the list
        item_found = False
        # loop over all items list
        for index, i in enumerate(items):
            # if the item which need to updated has the same id of the one in the list
            if i.get_item_id() == item.get_item_id():
                # Update the item's with the new availability status
                i.set_available(item.check_availability())
                
                # if the item is not reserved, clear the reserved_by_id
                # make this if to handle magazine case
                # so first will check if the item has these two methods
                if hasattr(i, 'clear_reserved') and hasattr(item, 'get_reserved_by'):
                    if item.get_reserved_by() is None:
                        i.clear_reserved()
                item_found = True
                break

        # if didn't find the item, raise an error
        if not item_found:
            raise ItemNotFoundError(f"Item {item.get_title()} not found in items list")

        # try to save the changes to the file
        if not store_items(items):
            raise IOError("❌ Failed to save item changes to file...")

        return True
    
    except ItemNotFoundError as e:
        print(e)
        return False
    
    except Exception:
        print("❌ Failed to update items...")
        return False