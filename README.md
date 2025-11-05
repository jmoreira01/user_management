# User Management System 🛡️

A lightweight CLI user manager in Python, colorful and terminal-friendly. Register, edit, delete, and list users with secure passwords (auto-generated or manual, strength-checked and unique). In-memory storage—great for prototypes or quick tests, no databases or hassle. Runs on any OS (Windows/Linux/Mac), with ANSI colors to keep it from being boring.

## ✨ Features
- **User Registration**: Unique username + password (auto-gen with uppercase/lowercase/digits/symbols, 8-16 chars) or manual (validates length, allowed chars, and uniqueness).
- **Password Strength**: Rates based on diversity (Strong/Medium/Weak, color-coded in terminal).
- **Edit User**: Change username or password (removes old one from used set).
- **View Info**: Shows username, masked password (****), and strength.
- **Delete User**: With confirmation, wipes everything (including password history).
- **List All**: Formatted table, sorted by username.
- **Colorful UI**: Purple headers, green successes (✓), red errors (✗), yellow warnings (⚠)—ANSI codes for flair.
- **Basic Security**: Globally unique passwords, hidden input via `getpass`, random shuffle for generation.

Built by [jmoreira01](https://github.com/jmoreira01) in collaboration with a fellow coder.
