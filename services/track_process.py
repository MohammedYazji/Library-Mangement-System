"""
This track_process module: which organize the code a little bit,
and make the main module more readable and simple

so this module will make the main module interact with other modules,
using simpler functions to simple the process and make the code nice.
"""
from colorama import Fore, Style # to display colors and styles to the CLI
from models.user import User
from models.library import Library
from models.book import Book
from models.dvd import DVD
from models.magazine import Magazine
from services import display, storage, validators
from Exceptions.exceptions import ItemCanNotReserve, ItemNotAvailableError, ItemNotFoundError

# Initialize the Library_object and store users, items as an attributes
def initialize_library():
    """
    load all data of users and items when start the application

    then make an instance from Library to access Library methods later

    Returns:
        tuple: returns a tuple contains:
            - users (list): list of all users instances (User_objects)
            - items (list): list of all items instances (Items_objects)
            - library_manager (Library): returns the Library object which will use it to access the library methods
    """

    # create an object from the `Library` and give it's constructor users, items as arguments from JSON Files
    library_manager = Library(storage.load_users(), storage.load_items())

    # get the private __users attribute using get_users
    users = library_manager.get_users()
    # get the private __items attribute using get_users
    items = library_manager.get_items()

    return users, items, library_manager

# This function handle the searching process
def handle_searching(users, items):
    """
    Make the user Desides which search methods want to choose (by title, or search by type)

    Display the search methods using `display_search_methods()` function,
    if the choise 1 => call 'search_by_title()' function
    and if the choise 2 => call 'search_by_type()' function.

    Args:
        items (list): the list of items instances
    """

    # display search methods (title, or type)
    search_type = display.display_methods('Search by Title', 'Search by Type','search based on')

    # handle searching by title
    if search_type == 1:
        search_query = input('\n✒️ Please enter a title: ').strip().lower()
        storage.search_by_title(search_query, items, users)
    
    # handle searching by type
    elif search_type == 2:
        search_query = input('\n✒️ Please enter a type: ').strip().lower()
        storage.search_by_type(search_query, items, users)

# This function handle register a new user process by dealing with
def register_user(users):
    """
    handle register a new user

    first gets the new user information using => `get_new_user_info()` function,
    after that makes a new User instance, and append it in the list of all users,
    finally updated this list of all users,
    using `store_users()` function

    Args:
        users (list): the list of all users
    """
    # get the email and the name of the new user after validation
    email, name = display.get_new_user_info(users, 'Your')
    
    # create a new user
    new_user = User(name, email)
    # then append the new user users list to store it later using `store_users()` function
    users.append(new_user)

    # save the new users_data into the JSON file
    if storage.store_users(users):
        # using colorama package to print an ouput with red color using `Fore`
        print(f'\n🎉 {name} now you are a member on the library\n🆔 your ID is: {new_user.get_display_id()} {Fore.RED + '[PLEASE SAVE IT]'}')
        # then reset the style to the default again
        print(Style.RESET_ALL)
    else:
        print('❌ Faild added the user...')

# handle the borrowing and return process
def handle_borrow_return(users, items, library_manager):
    """
    Method to handle the borrowing and return process easily

    Receive the choice from the user using `display_methods()` function
    if the choice is 1 call => `borrow_item()` function,
    else if the choice is 2 call => `return_item()` function
    Args:
        users (list): the list of all users instances
        items (list): the list of all items instances
        library_manager (Library): the library object we used to access the library methods
    """
    # get the choice from the user after validate the input
    choice = display.display_methods('Borrow an item', 'Return an item', 'Borrow / Return an item')

    # handle borrowing an item process
    if choice == 1:
        borrow_item(users, items, library_manager)
    # handle returning an item process
    elif choice == 2:
        return_item(users, items, library_manager)

# Borrowing Item
def borrow_item(users, items, library_manager):
    """
    Borrowing an item using the Library method => `borrow_item()`

    get the user and the item by their ID's using => `get_user_item_info()` function,
    then make the borrowing process using the library method `borrow_item()` by access it
    using the `library_manager` object
    After the borrowing process should update the users and items lists

    Args:
        users (list): list of users instances
        items (list): list of items instances
        library_manager (Library): the library object we used to access the library `borrow_item()` method
    """
    # get the user and item after validation
    user, item = display.get_user_item_info(users, items, 'Borrow')

    # if one of them doesn't exist using get_user_item_info => stop the function
    if not user or not item:
        return

    # make the borrowing process using `borrow_item()` method
    is_success = library_manager.borrow_item(user, item)

    # try to update changes in items and users lists
    if is_success:
        # pass the new user status to update it in the list of all users
        if not storage.update_users(users, user):
            print("\n❌ Failed to save user changes...")
            return
        # pass the new item status to update it in the list of all items
        # after any borrow or reserved I need to update the lists to keep sync
        if not storage.update_items(items, item):
            print("\n❌ Failed to save item changes...")
            return
        
        print(f"\n✅ {user.get_name()} borrowed {item.get_title()} successfully.")
        return
    else:
        # display the unavailable to borrow message
        try:
            display.display_not_available_to_have(users, item, "borrowed")
        except ItemNotAvailableError as e:
            print(e)

# Return an Item
def return_item(users, items, library_manager):
    """
    Returning an item to the library using Library method => `return_item()`

    get the user and the item by their ID's using => `get_user_item_info()` function,
    then make the returning process using the library method `return_item()` by access it
    using the `library_manager` object
    After the returning process should update the users and items lists

    Args:
        users (list): list of users instances
        items (list): list of items instances
        library_manager (Library): the library object we used to access the library `return_item()` method
    """

    # get the user and item after validating 
    user, item = display.get_user_item_info(users, items, 'Return')

    # if one of them dosen't exist using get_user_item_info => stop the function
    if not user or not item:
        return

    # make the Returning process using `return_item()` method
    is_success = library_manager.return_item(user, item)

    # if success please update the users and items lists to keep all data sync togother
    if is_success:
        # pass the new user status to update it in the list of all users
        if not storage.update_users(users, user):
            print("\n❌ Failed to save user changes...")
            return
        # pass the new item status to update it in the list of all items
        if not storage.update_items(items, item):
            print("\n❌ Failed to save item changes...")
            return
        
        print(f"\n✅ {user.get_name()} Returned {item.get_title() }, and now it's available again.")
    else:
        print(f'\n❌ Returning {item.get_title()} Faild...')

# handle the Reservation and cancel_reservation proccess
def handle_reserve_cancel(users, items, library_manager):
    """
    Method to handle the Reservation and cancel_reservation proccess easily

    Receive the choice from the user using `display_methods()` function
    if the choice is 1 call => `reserve_item()` function,
    else if the choice is 2 call => `cancel_resrvation()` function
    Args:
        users (list): the list of all users instances
        items (list): the list of all items instances
        library_manager (Library): the library object we used to access the library methods
    """

    # get the choice from the user after validate the input
    choice = display.display_methods('Reserve', 'Cancel Reservation', 'Reserve / Cancel Reservation')

    # handle the reservation process
    if choice == 1:
        reserve_item(users, items, library_manager)
    # handle cancel_reservation process
    elif choice == 2:
        cancel_resrvation(users, items, library_manager)

# reserve an item
def reserve_item(users, items, library_manager):
    """
    Reserving an item using Library method => `make_reservation()`

    get the user and the item by their ID's using => `get_user_item_info()` function,
    then make the Reservation process using the library method `make_reservation()` by access it
    using the `library_manager` object
    If item type is Magazine => raise a custom exeption `Item_Can_not_reserve`.
    After the Reservation process done, should update the users and items lists.

    Args:
        users (list): list of users instances
        items (list): list of items instances
        library_manager (Library): the library object we used to access the library `make_reservation()` method

    Raises:
        Item_Can_not_reserve: Raise an error if the user want to reserve a magazine
    """
    # get the user and item after validating  
    user, item = display.get_user_item_info(users, items, 'Reserve') 

    # if one of them dosen't exist using get_user_item_info => stop the function
    if not user or not item:
        return

    try:
        # if user want to reserve a magazine => raise custom `Item_Can_not_reserve`
        if item.__class__.__name__ == 'Magazine':
            raise ItemCanNotReserve("❌ You can't reserve a magazine!")
        
        # make the reservation using `make_reservation()` using the library object
        is_success = library_manager.make_reservation(user, item)

        # if the reservation procces done
        # update the users, and items list to keep all data in sync
        if is_success:
            # pass the new user status to update it in the list of all users
            if not storage.update_users(users, user):
                print("\n❌ Failed to save user changes...")
                return
            # pass the new item status to update it in the list of all items
            if not storage.update_items(items, item):
                print("\n❌ Failed to save item changes...")
                return

            print(f"\n✅ {user.get_name()} Reserved the {item.get_title() }")
            return
    
        else:
            # display that the item already not available from another user
            try:
                display.display_not_available_to_have(users, item, "reserved")
            except ItemNotAvailableError as e:
                print(e)

    except ItemCanNotReserve as e:
        print(e)

# cancel the reservation
def cancel_resrvation(users, items, library_manager):
    """
    cancel the reservation using Library method => `cancel_reserve()`

    get the user and the item by their ID's using => `get_user_item_info()` function,
    then make the canceling process using the library method `cancel_reserve()` by access it
    using the `library_manager` object
    After the canceling process should update the users and items lists

    Args:
        users (list): list of users instances
        items (list): list of items instances
        library_manager (Library): the library object we used to access the library `cancel_reserve()` method
    """
    # get the user and item after validation
    user, item = display.get_user_item_info(users, items, 'Cancel Reservation')

    if not user or not item:
        return

    # make the cancel reservation using `cancel_reserve()` using the library object
    is_success = library_manager.cancel_reserve(user, item)

    # if the procces done
    # update the users, and items list to keep all data in sync
    if is_success:
        # pass the new user status to update it in the list of all users
        if not storage.update_users(users, user):
            print("\n❌ Failed to save user changes...")
            return
        # pass the new item status to update it in the list of all items
        if not storage.update_items(items, item):
            print("\n❌ Failed to save item changes...")
            return

        print(f"\n✅ {user.get_name()} cancel the reservation of {item.get_title() }")
    
    else:
        print(f'\n❌ Cancel The Reservation of {item.get_title()} faild...')

# handle adding, removing items / users from items JSON File
def handle_admin(users, items, library_manager):
    """
    Method to handle the admin actions (add / remove an item or user)

    first ask the user to input the admin password if true
    Receive the choice from the user using `display_methods()` function
    if the choice is 1 so handle items:
        if choice is 1 call => `add_an_item()`
        else if choice is 2 call => `remove_an_item()`

    if the choice is 2 so handle users:
        if choice is 1 call => `add_a_user()`
        else if choice is 2  => `remove_a_user()`

    Args:
        users (list): the list of all users instances
        items (list): the list of all items instances
        library_manager (Library): the library object we used to access the library methods
    """
    is_admin = display.get_admin_password()

    if is_admin == 'admin':
        # get the choice from the user after validate the input
        choice = display.display_methods('Manage Library Items', 'Manage Library Users', 'to manage items, or users')
        
        # Item or User
        if choice == 1:
            # Add or Remove (items)
            sub_choice = display.display_methods('Add a new item', 'Remove an existing item', 'Add / Remove an item')
            if sub_choice == 1:
                add_an_item(items, library_manager)
            elif sub_choice == 2:
                remove_an_item(users, items, library_manager)
        elif choice == 2:
            # Add or Remove (users)
            sub_choice = display.display_methods('Add a user (Admin)', 'Remove a user (Admin)', 'Add / Remove a user (Admin)')
            if sub_choice == 1:
                add_a_user(users, library_manager)
            elif sub_choice == 2:
                remove_a_user(users, library_manager)
    else:
        return

# add an item (ADMIN)
def add_an_item(items, library_manager):
    """
    Add an item by the admin using the library method `add_item()` method

    Receives the item information from `get_admin_item_info()` after validate it's not empty
    and the type is valid, then make an instance from this information using items constructors
    based on the input type, then add the new item to the list of items using `add_item()` library method
    then store the items list again in the items file using `store_items()` function, to update it and keep sync

    Args:
        items (list): the list of all items
        library_manager (Library): An instance from Library, to access `add_item()` Library method
    """
    # get the item info
    item_type, title, author = display.get_admin_item_info('Add')

    # Check if item already exists
    for item in items:
        # for each item in the list if has the same type, title, author as the input item (It's exist before)
        if item.get_type().lower() == item_type.lower() and item.get_title().lower() == title.lower() and item.get_author().lower() == author.lower():
            print("\n❌ The Item Already Exist...")
            return

    # Create new item based on type
    new_item = None
    if item_type == 'Book':
        new_item = Book(title, author, True)
    elif item_type == 'DVD':
        new_item = DVD(title, author, True)
    elif item_type == 'Magazine':
        new_item = Magazine(title, author, True)
    else:
        print("\n❌ Invalid item type...")
        return

    # Add the new item to the library
    if new_item:
        library_manager.add_item(new_item)

        # I updated it manually above
        # just store all items including the new one
        if not storage.store_items(items):
            print("\n❌ Failed to save item changes...")
            return
        
        print(f"\n✅ {title} Added successfully.")
        return

# remove an existing item (ADMIN)
def remove_an_item(users, items, library_manager):
    """
    Remove an existing item by the admin using the library method `remove_item()` method

    Receives the item information from `get_admin_item_info()` after validate it's not empty
    and the type is valid, then check the items list if the item exist so => remove it from the list
    using the Library method `remove_item()`, then try to update the items list
    and store the new one without the one which we removed

    Args:
        items (list): the list of all items
        users (list): the list of all users
        library_manager (Library): An instance from Library, to access `remove_item()` Library method
    """
    try:
        # get the item info
        item_type, title, author = display.get_admin_item_info('Remove')

        # Check if item already exists
        item_found = False
        for item in items:
            # if the item already exist => remove it from the items list
            if item.get_type().lower() == item_type.lower() and item.get_title().lower() == title.lower() and item.get_author().lower() == author.lower():
                if hasattr(item, 'get_reserved_by'):
                    for user in users:
                        # Check if item is reserved by this user
                        if user.get_user_id() == item.get_reserved_by():
                            raise Exception(f"\n❌ Cannot remove item: {item.get_title()} is reserved by {user.get_name()}")
                        
                        # Check if item is borrowed by this user
                        for borrowed_item in user.get_borrowed_items():
                            if borrowed_item['item_id'] == item.get_item_id():
                                raise Exception(f"\n❌ Cannot remove item: {item.get_title()} is borrowed by {user.get_name()}")
                        
                    # If we get here, item is not reserved or borrowed by anyone
                    library_manager.remove_item(item)
                    item_found = True
                
                # I updated it manually above
                # Just store all items without the one we removed
                if not storage.store_items(items):
                    print("\n❌ Failed to save item changes...")
                    return
                
                print(f"\n✅ {title} Removed successfully.")
                return

        if not item_found:
            raise ItemNotFoundError("\n❌ Item does not exist...")

    except ItemNotFoundError as e:
        print(e)
    
    except Exception as e:
        print(e)

# Add a user (ADMIN)
def add_a_user(users, library_manager):
    """
    Add a new user to the library system.
    
    Args:
        users (list): List of all users
        library_manager (Library): An instance from Library, to access `add_user()` Library method
    
    Returns:
        bool: true if user was added successfully, otherwise false
    """
    try:
        # Get user information using existing function that handles all validation
        email, name = display.get_new_user_info(users, 'The')
        
        # Create new user instance
        new_user = User(name, email)
        
        # Add the user to the library
        if not library_manager.add_user(new_user):
            raise Exception("\n❌ Failed to add user!")
            
        # Update storage
        if not storage.store_users(users):
            raise Exception("\n❌ Failed to save user information!")
            
        # Display the success message
        print(f'\n✅ The Admin: Successfully added a new user:\n')
        print(f'👲 Name: {name}')
        print(f'📧 Email: {email}')
        print(f'🆔 User ID: {new_user.get_display_id()}')
        return True
        
    except Exception as e:
        print(e)
        return False

# remove a user (ADMIN)
def remove_a_user(users, library_manager):
    """
    Remove a user from the library system.
    
    Args:
        users (list): List of all users
        library_manager (Library): Library instance to manage users
    
    Returns:
        bool: True if user was removed successfully, False otherwise
    """
    try:
        # Get user ID to remove
        user_id = input("\nEnter user ID to remove: ").strip()
        
        # Validate user ID using the user id validation function
        user_to_remove = validators.user_id_validation(user_id, users)
        if not user_to_remove:
            return False
            
        # Check if user has any borrowed or reserved items
        borrowed_items = user_to_remove.get_borrowed_items()
        reserved_items = user_to_remove.get_reserved_items()
        
        if borrowed_items:
            raise Exception(f"\n❌ Cannot remove user: {user_to_remove.get_name()} has {len(borrowed_items)} borrowed item(s)")
            
        if reserved_items:
            raise Exception(f"\n❌ Cannot remove user: {user_to_remove.get_name()} has {len(reserved_items)} reserved item(s)")
            
        # Remove the user
        if not library_manager.remove_user(user_to_remove):
            raise Exception("\n❌ Failed to remove user!")
            
        # Update storage
        if not storage.store_users(users):
            raise Exception("\n❌ Failed to save user data!")
            
        print(f"\n✅ User {user_to_remove.get_name()} removed successfully!")
        return True
        
    except Exception as e:
        print(e)
        return False
