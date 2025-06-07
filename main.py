"""
The main module: The Start point of The Library Management System.

Handle the interaction of the user with the application 
"""
from services import display, track_process

# initialize the application using => `initialize_library()`
# and load the data from the JSON Files
users, items, library_manager = track_process.initialize_library()

# The Main Loop [To keep displaying the menu]
while True:
    # display the menu and get the choice (1 - 7)
    choice = display.display_welcome_message()

    # view all available items
    if choice == 1:
        display.display_available_items(users, items)

    # search an items based on title, or type
    elif choice == 2:
        track_process.handle_searching(users, items)

    # register a new user
    elif choice == 3:
        track_process.register_user(users)

    # Borrow an item / return an item
    elif choice == 4:
        track_process.handle_borrow_return(users, items, library_manager)

    # Reserve an item / cancel reservation
    elif choice == 5:
        track_process.handle_reserve_cancel(users, items, library_manager)
        
    # Admin: Add/Remove Items/Users (As Admin)
    elif choice == 6:
        track_process.handle_admin(users, items, library_manager)
        
    # Exit and Save
    elif choice == 7:
        print("💡 Thanks for using my Library Management System.")
        exit()
