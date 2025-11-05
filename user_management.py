import random
import string
import os
from getpass import getpass

# Color codes for terminal output formatting
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


users = {}  # Dictionary to store username: [password, strength]
used_passwords = set()  # Set to track all used passwords for uniqueness
# list of characters for password generation
characters = list(
    string.ascii_uppercase
    + string.ascii_lowercase
    + string.digits
    + string.punctuation
)

def clear_screen():
    #Clear the terminal screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    #Print a formatted header with the given title
    print(f"\n{Colors.CYAN}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.PURPLE}{title:^50}{Colors.END}")
    print(f"{Colors.CYAN}{'='*50}{Colors.END}\n")

def print_success(message):
    #Print a success message with green checkmark
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    #Print an error message with red cross
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message):
    #Print a warning message with yellow warning symbol
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def print_info(message):
    #Print an info message with blue information symbol
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

def print_menu_option(number, description):
    #Print a formatted menu option with number and description
    print(f"{Colors.BOLD}{Colors.CYAN}{number}.{Colors.END} {description}")

def password_generator():

    # Generate a secure random password that meets complexity requirements

    while True:
        # Ensure password contains at least one of each required character type
        requirements = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice(string.punctuation)
        ]
        # Add random extra characters for length variation (8-16 total characters)
        extra_length = random.randint(4, 12)
        extra_chars = random.choices(characters, k=extra_length)
        
        # Combine and shuffle all characters
        password = requirements + extra_chars
        random.shuffle(password)
        final_pass = ''.join(password)
        
        # Ensure password uniqueness
        if final_pass not in used_passwords:
            used_passwords.add(final_pass)
            return final_pass

def password_strength(password):

    #Evaluate the strength of a password based on character diversity

    # Check for presence of different character types
    has_uppercase = any('A' <= char <= 'Z' for char in password)
    has_lowercase = any('a' <= char <= 'z' for char in password)
    has_digit = any('0' <= char <= '9' for char in password)
    has_symbol = any(char in string.punctuation for char in password)
    
    # Score based on character type diversity
    points = sum([has_uppercase, has_lowercase, has_digit, has_symbol])
    
    # Return color-coded strength rating
    if points == 4:
        return f"{Colors.GREEN}Strong{Colors.END}"
    elif points == 3:
        return f"{Colors.YELLOW}Medium{Colors.END}"
    else:
        return f"{Colors.RED}Weak{Colors.END}"

def username_exists(username):

    #Check if a username already exists in the system

    return username in users

def user_registration():
    #Register a new user with username and password
    print_header("USER REGISTRATION")
    
    # Get and validate username
    username = input(f"{Colors.BOLD}Enter your Username:{Colors.END} ").strip().lower()
    if not username:
        print_error("Username cannot be empty.")
        return
    
    if username_exists(username):
        print_error(f"Username '{username}' already exists.")
        return

    # Password option selection
    print(f"\n{Colors.BOLD}Choose password option:{Colors.END}")
    print_menu_option("1", "Auto-generate secure password")
    print_menu_option("2", "Enter your own password")
    
    choice = input(f"\n{Colors.BOLD}Select option (1 or 2):{Colors.END} ").strip()
    
    if choice == '1':
        # Auto-generate password
        print_info("Generating secure password...")
        password = password_generator()
        print_success(f"Generated password: {Colors.BOLD}{password}{Colors.END}")
    elif choice == '2':
        # Manual password entry with validation
        while True:
            password = getpass(f"{Colors.BOLD}Enter your password:{Colors.END} ")
            if not password:
                print_error("Password cannot be empty.")
                continue
            if len(password) < 8:
                print_error("Password must be at least 8 characters.")
                continue
            if not all(i in characters for i in password):
                print_error(f"Only allowed: letters, digits, and symbols: {string.punctuation}")
                continue
            if password in used_passwords:
                print_error("This password is already used by another user. Choose another.")
                continue
            used_passwords.add(password)
            break
    else:
        print_error("Invalid option!")
        return
        
    # Evaluate password strength and store user data
    strength = password_strength(password)
    users[username] = [password, strength]
    print_success(f"User '{username}' registered successfully!")
    print(f"Password Strength: {strength}")

def user_info():
    #Display information for a specific user
    print_header("USER INFORMATION")
    
    # Get and validate username
    username = input(f"{Colors.BOLD}Enter Username:{Colors.END} ").strip().lower()
    if not username_exists(username):
        print_error(f"Username '{username}' not found.")
        return
    
    # Retrieve user data
    password, strength = users[username]
    
    # Display user information (password is masked)
    print(f"\n{Colors.CYAN}{'─'*40}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.PURPLE}User Details:{Colors.END}")
    print(f"{Colors.CYAN}{'─'*40}{Colors.END}")
    print(f"{Colors.BOLD}Username:{Colors.END} {username}")
    print(f"{Colors.BOLD}Password:{Colors.END} {'*' * len(password)}")
    print(f"{Colors.BOLD}Strength:{Colors.END} {strength}")
    print(f"{Colors.CYAN}{'─'*40}{Colors.END}")

def edit_user():
    """Edit an existing user's username or password"""
    print_header("EDIT USER")
    
    # Get and validate existing username
    old_username = input(f"{Colors.BOLD}Enter username to edit:{Colors.END} ").strip().lower()
    if not username_exists(old_username):
        print_error(f"Username '{old_username}' not found.")
        return

    # Edit option selection
    print(f"\n{Colors.BOLD}What do you want to edit?{Colors.END}")
    print_menu_option("1", "Change username")
    print_menu_option("2", "Change password")
    
    option = input(f"\n{Colors.BOLD}Select option (1 or 2):{Colors.END} ").strip()

    if option not in ["1", "2"]:
        print_error("Invalid option. Nothing changed.")
        return

    # Store current user data
    old_password, old_strength = users[old_username]
    new_username = old_username
    new_password = old_password
    new_strength = old_strength

    # Username change workflow
    if option == '1':
        while True:
            new_username_input = input(f"{Colors.BOLD}New username:{Colors.END} ").strip().lower()
            if not new_username_input:
                print_error("Username cannot be empty.")
                continue
            if new_username_input == old_username:
                print_warning("Same as old username. No change made.")
                return
            if username_exists(new_username_input):
                print_error(f"Username '{new_username_input}' already exists.")
                continue
            new_username = new_username_input
            break

    # Password change workflow
    elif option == '2':
        # Remove old password from used passwords set
        used_passwords.discard(old_password)

        print(f"\n{Colors.BOLD}Choose new password option:{Colors.END}")
        print_menu_option("1", "Auto-generate secure password")
        print_menu_option("2", "Enter your own password")
        
        password_option = input(f"\n{Colors.BOLD}Select option (1 or 2):{Colors.END} ").strip()

        if password_option == '1':
            # Auto-generate new password
            print_info("Generating new password...")
            new_password = password_generator()
            print_success(f"New password: {Colors.BOLD}{new_password}{Colors.END}")
        elif password_option == '2':
            # Manual password entry with validation
            while True:
                new_password_input = getpass(f"{Colors.BOLD}Enter new password:{Colors.END} ")
                if not new_password_input:
                    print_error("Password cannot be empty.")
                    continue
                if len(new_password_input) < 8:
                    print_error("Password must be at least 8 characters.")
                    continue
                if not all(i in characters for i in new_password_input):
                    print_error(f"Only allowed: letters, digits, and symbols: {string.punctuation}")
                    continue
                if new_password_input in used_passwords:
                    print_error("This password is already in use. Choose another.")
                    continue
                used_passwords.add(new_password_input)
                new_password = new_password_input
                break
        else:
            print_error("Invalid option.")
            return

        # Evaluate new password strength
        new_strength = password_strength(new_password)

    # Update user data in storage
    if new_username != old_username:
        del users[old_username]
    users[new_username] = [new_password, new_strength]
 
    print_success("User updated successfully!")
    # Display changes made
    if new_username != old_username:
        print(f"Username: {Colors.BOLD}'{old_username}' → '{new_username}'{Colors.END}")
    if new_password != old_password:
        print(f"Password Strength: {new_strength}")

def remove_user():
    #Remove a user from the system
    print_header("REMOVE USER")
    
    # Get and validate username
    username = input(f"{Colors.BOLD}Enter username to remove:{Colors.END} ").strip().lower()
    if not username:
        print_error("Username cannot be empty.")
        return
    if not username_exists(username):
        print_error(f"Username '{username}' does not exist.")
        return
    
    # Confirmation for deletion
    confirm = input(f"{Colors.RED}{Colors.BOLD}Are you sure you want to delete '{username}'? (y/N):{Colors.END} ").strip().lower()
    if confirm != 'y':
        print_warning("Deletion cancelled.")
        return
 
    # Remove user data from storage
    password = users[username][0]
    used_passwords.discard(password)
    del users[username]
    print_success(f"User '{username}' deleted successfully.")

def list_all_users():
    #Display all registered users in a formatted table
    print_header("ALL USERS")

    if len(users) == 0:
        print_info("No users registered.")
        return
    
    # Print user table header
    print(f"{Colors.BOLD}{'Username':<20} {'Password Strength':<15}{Colors.END}")
    print(f"{Colors.CYAN}{'─'*40}{Colors.END}")
    
    # Print each user's data
    for username in sorted(users.keys()):
        strength = users[username][1] 
        print(f"{username:<20} {strength:<15}")
    
    print(f"{Colors.CYAN}{'─'*40}{Colors.END}")
    print_info(f"Total users: {len(users)}")

def main_menu():
    while True:
        clear_screen()
        print_header("USER MANAGEMENT SYSTEM")
        
        # Display menu options
        print_menu_option("1", "Add New User")
        print_menu_option("2", "View User Information")
        print_menu_option("3", "Edit User")
        print_menu_option("4", "Remove User")
        print_menu_option("5", "List All Users")
        print_menu_option("6", "Exit")
        
        print(f"\n{Colors.CYAN}{'='*50}{Colors.END}")
        
        # Get user menu selection
        choice = input(f"\n{Colors.BOLD}Select an option (1-6):{Colors.END} ").strip()

        # Execute corresponding function based on user choice
        if choice == '1': 
            user_registration()
        elif choice == '2': 
            user_info()
        elif choice == '3': 
            edit_user()
        elif choice == '4': 
            remove_user()
        elif choice == '5': 
            list_all_users()
        elif choice == '6':
            print_header("GOODBYE!")
            print_success("Thank you for using User Management System!")
            break
        else:
            print_error("Invalid option! Please try again.")
        
        # Pause before returning to menu (except when exiting)
        if choice != '6':
            input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.END}")

# Program entry point
if __name__ == "__main__":
    main_menu()
