"""
This display module: has all methods related to display messages
and data to the screen with a nice formatting
"""
from services import validators
from Exceptions.exceptions import FileIsEmptyError, ItemNotAvailableError, ItemNotFoundError

# display welcome message, and the menu
def display_welcome_message():
    """
    Displays the welcome message, and the menu

    Return the choice of the user from the menu as an integer,
    after validate it using `int_validation()` method

    Returns:
        `int`: Returns The Choice (1 - 7)
    """
    print()
    print('='  * 30)
    choice = input('👋 Welcome to the Library System\n1. View all available items ✅ \n2. Search item by title or type 🔍 \n3. Register as a new user 🆕 \n4. Borrow / Return an item 📚 \n5. Reserve / cancel reservation an item 🪧 \n6. Admin: Add/Remove Items/Users ⚙️ \n7. Exit 🙋 \n> ')
    choice = validators.int_validation(choice, 1, 7, 'choice')

    return choice

# Display the avaliable items
def display_available_items(users, items):
    """
    Displays all items with it's status (available or, not) 

    Receives all items as an argument, then print the avaliable items 
    based on `check_availability()` value Which is each item can access it from 
    the parent LibraryItem

    Args:
        users (list): Receives list of users instances
        items (list): Receives list of items instances
    """

    try:
        # if the list of items is empty raise custom exception => `FileIsEmptyError`
        if not items:
            raise FileIsEmptyError('\n❌ No items data yet, items file is empty...')

        # make dictionary to keep tracking the number of the avaliable items for each Type
        items_dict = {'Book': 0, 'Magazine': 0, 'DVD': 0}

        # count the avaliable items for each type and store them in the dictionary above `item_dict`
        for item in items:
            is_avaliable = item.check_availability()
            item_type = item.get_type()

            # if available please add one in items_dict for this type
            if is_avaliable:
                items_dict[item_type] += 1

        # if there is no any available item, raise custom Error =>  `ItemNotAvailableError`
        is_no_items_available = True
        for count in items_dict.values():
            if count != 0:
                is_no_items_available = False
                break
        
        if is_no_items_available:
            raise ItemNotAvailableError('\n❌ No items available at the moment')


        print("\n--- The avaliable Items is ---\n")
        # loop over the dict `item_dict` print how many items avaliable of each type
        for key, value in items_dict.items():
            print(f"\n{'📚' if key == 'Book' else '📝' if key == 'Magazine' else '📀'} {value} {key}{"s" if value > 1  else ""} is available: ")
            print('=' * 30)
            # Here I don't raise an error to continue the application flow, and just print a message
            if value == 0:
                print(f"\n❌ There's no any {key} Avaliable!")

            # then inside each loop on dict, loop over the items in items_data
            # I know it's a nested loop with O(n^2) but 😅
            # and if the item is avaliable at the same time the type same as dict-key
            # call => `display_info(users)` method that each item override this abstract method
            else:
                for item in items:
                    is_avaliable = item.check_availability()
                    item_type = item.get_type()

                    if item_type == key:
                        print(item.display_info(users))

    except FileIsEmptyError as e:
        print(e)

    except ItemNotAvailableError as e:
        print(e)

# display methods to let the user choose one of them
def display_methods(first_choice, second_choice, message):
    """
    Display the methods of specific process (e.g, (searching => title, type), (borrow, return), etc...)

    Display the methods that the user can continue the process based on them,
    and receive an input from user,
    then returns it after ensure it's valid using `int_validation()` function

    Args:
        first_choice (str): the text message will display to the user of the first choice
        second_choice (str): the text message will display to the user of the second choice
        message (str): the text message will display for the header of the question

    Returns:
        int: Returns The Choice (1 - 2)
    """
    search_type =  input(f'\nDo you like to {message}:\n1. {first_choice}\n2. {second_choice}\n> ')
    return validators.int_validation(search_type, 1, 2, 'choice')

# display the searching result
def display_search_result(search_query, search_result, users):
    """
    Displays the searching result

    Receiving the search_result as a list contains all items matches the searching process,
    then displays all the item information in a nice print statement

    Args:
        search_reult (list): list contains all items matches the searching process
        users (list): receive a list of users instances to pass it to `display_info()` method
    """

    try:
        print(f'\n---🔎 the Searching result of ({search_query})---')
        # if there's no item with the same search_query raise custom Error => `ItemNotFoundError`
        if not search_result:
            raise ItemNotFoundError('\n❌ No Items found...')

        # else print the search reult with all items information
        # using `display_info()` item method
        for item in search_result:
            print(item.display_info(users))

    except ItemNotFoundError as e:
        print(e)

# Receives the new user information
def get_new_user_info(users, as_who):
    """
    Receives the new user information from the user

    Get the new user information like => the email, and the name, then validate them using => `email_validation()` function, and `empty_input_validation()` function.

    and return them after the valiadtion process done.

    Returns:
        tuple: returns a tuple contains the valid_email, and name
    """
    print("please enter the following: ")

    email = input(f"\n- {as_who} Email: ").strip()
    # validate the email
    email = validators.email_validation(email, users)
    name = input(f"\n- {as_who} Name: ").strip()
    # validate the name
    name = validators.empty_input_validation(name, 'name')

    return email, name

# Receives the user id and the item id to make the brrowing process
def get_user_item_info(users, items, message):
    """
    Receive the user id and the item id from the user.

    Receive the user id and the item id from the user,
    then validate them using `user_id_validation()`, and `item_id_validation()`
    functions. if the the user id dosen't exist => return and stop the function

    Args:
        users (list): list of users instances
        items (list): list of items instances
        message (str): the type of the process (e.g, borrow, reserve, return, ....)

    Returns:
        tuple: Returns a tuple contains:
                - user (User): Returns the `user` if the ID is Exist, otherwise return `None`
                - item (Item): Returns the `item` if the ID is Exist, otherwise return `None`
    """
    print(f'To {message} an item you should enter the following: ')

    user_id = input('- your user id: ').strip()
    # validate the user_id using `user_id_validation()`
    user = validators.user_id_validation(user_id, users)

    # if there'e no exist user return None to stop implementing the function
    # to prevent receive the item_id
    if not user:
        return None, None
    
    item_id = input('- the item id: ').strip()
    # validate the user_id using `item_id_validation()`
    item = validators.item_id_validation(item_id, items)

    # if there'e no exist item return None to stop implementing the function
    if not item:
        return None, None
    
    # return both the user, item as a tuple if the both exist...
    return user, item

# Displays message when the item reserved, or borrowed by another one
def display_not_available_to_have(users, item, message):
    """
    Displays a message if the item is already taken by another user

    Receiving the users list and the item, then loop over each user in the users list,
    if the item id exists in the user borrowed_items list => get the usser name to print it
    else if the user id exists in the item reserved by => get the user id to print it

    Args:
        users (list): list of users to search based on it
        item (LibraryItem): Receive the item to check if borrowed, or reserved by someone else
        message (str): The message to print "borrowed" or "reserved"
        
    Raises:
        ItemNotAvailableError: If the item is already borrowed or reserved
    """
    borrowed_by_name = None
    reserved_by_name = None
    for user in users:
        # check is the item borrowed by someone else
        user_borrowed_items = user.get_borrowed_items()
        for i in user_borrowed_items:
            if i['item_id'] == item.get_item_id():
                borrowed_by_name = user.get_name()

        # Check for reserved status
        if user.get_user_id() == item.get_reserved_by():
            reserved_by_name = user.get_name()

    # intial value
    item_status = "not available"
    if borrowed_by_name:
        item_status = item_status +  f", borrowed by {borrowed_by_name}"
    if reserved_by_name:
        item_status = item_status + f", reserved by {reserved_by_name}"

    raise ItemNotAvailableError(f'\n❌ {message} {item.get_title()} Failed...\n {item.get_title()} is already {item_status}')

# Receives the admin password, and check it
def get_admin_password():
    """
    Display the password input field, and check the password using `check_admin()`

    Display the password input field to check if the admin is_admin,
    and receive an input from user,
    then returns true after ensure is an admin using `check_admin()` function

    Returns:
        str: Returns 'admin', 'stop' based on the validator function `check_admin()`
    """
    password = input('\n🔒 Please enter the admin password: ')
    return validators.check_admin(password)

# get the item info to add it or remove it from the admin
def get_admin_item_info(message):
    """
    Receives the item information and validate it;s not empty field then return them

    also validate if the type is valid

    Args:
        message (str): the process name to print (e.g, Add, remove an item)

    Returns:
        tuple: Returns a tuple contains:
                - item_type: the type of the item 
                - title: the title of the item 
                - author: the author of the item 
    """
    print(f'To {message} an item you should enter the following: ')

    item_type = input('- The Type of the Item: ').strip().capitalize()
    item_type = validators.type_validation(item_type)
    title = input('- The Title of the Item: ').strip()
    title = validators.empty_input_validation(title, 'item title')
    author = input('- The Author of the Item: ').strip()
    author = validators.empty_input_validation(author, 'item author')

    if item_type and title and author:
        return item_type, title, author