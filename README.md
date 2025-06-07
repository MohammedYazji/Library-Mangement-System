# Library Management System

## Started

- 💡 First, I recommend installing the Markdown Preview Enhanced extension to read this README in a nice format: [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)

A simple library system that helps you manage books, magazines, and DVDs.
You can borrow items, return items, and even reserve them for later.

## Table of Contents

- [What I learnt](#What-I-learnt)
- [Explain Project Modules](#Project-Modules)
- [How to use the app](#How-to-use-the-Library)
- [How to Run](#how-to-run-the-app)
- [Important Notes](#important-notes)
- [Help](#help)

## What I learnt

During this project, I learned many things using `Stack Overflow` and `GeeksforGeeks`:

- **Docstrings**: Used multi-line comments at the start of each method and class to make the code more readable and easier to track. When you hover over any method or class, you'll see its documentation.
- **UUID4**: I used Python uuid4 method from `uuid` module to generate unique IDs for library items.
- **Regular Expressions (REGAX)**: Used `re` module for to ensure that the input email is valid.
- **Class Methods**: Implemented `@classmethod` for converting data to a real instances
- **Name Mangling**: To access the calss attributes outside it, and sometimes i use protected attributes to avoid this Name mangling Issue in python
- **Colorama**: Used `colorama` package to add colors and styles to the CLI

## Project Modules

### Main Module

- `main.py`: The start point of the application
- Handles the main menu and user interaction flow

### Models

- `models/libraryitem.py`: Abstract class for all library items
- `models/reservable.py`: Interface for items that can be reserved (Book and DVD)
- `models/book.py`: Book class subclass of (LibraryItem, and Reservable interface)
- `models/magazine.py`: Magazine class subclass of (LibraryItem)
- `models/dvd.py`: DVD class implementation subclass of (LibraryItem, and Reservable interface)
- `models/user.py`: User class for managing library users
- `models/library.py`: library class for managing items and users

### Services

- `services/track_process.py`: track user actions link main with other modules
- `services/display.py`: Handles all screen output, inputs fields and menu displays
- `services/storage.py`: Dealing with JSON Files (users.JSON, items.JSON)
- `services/validators.py`: Input validation and, check the input's are valid.

### Exceptions

- `Exceptions/exceptions.py`: I made Custom exception classes for error handling, and raises errors

## How to use the Library

### Regular Users

1. First, create your account (Option 3 in the menu)
2. Save your User ID - you will need it later..
3. Browse available items (Option 1)
4. Search for specific items (Option 2)
5. Borrow or return items (Option 4)
6. Reserve items or cancel reservations (Option 5)

### Admin

- Use the admin password: `12345`
- Choose Option 6 in the main menu
- You can then:
  - Add, or remove items
  - Add, or remove users

## How to Run the app

1. Unzip the project folder
2. Install the required package => type this in your terminal:
   ```bash
   pip install colorama
   ```
3. Start the program:
   ```bash
   python main.py
   ```

## Important Notes

- The app saves your changes automatically
  - I save the changes after each process not when exit the program
- I change the CLI a little bit
  - after ask Dr. Refat to add cancel reservation, I made some changes to make the CLI
    simpler, and use emojies to make the app fun
- You can't borrow an item that's already borrowed, or reserved
- You can't reserve a magazine
- I just make the user input the first 8 characters from the ID, but the ID contains
  32 characters
- I use errors and exceptions to handle any issues

## Help?

If you face any problems:

- Make sure you've installed the colorama package
- Check that you're using the correct User ID
- Make sure you're using the right admin password `12345`
- Finally you can look at the JSON files to see how everything works
