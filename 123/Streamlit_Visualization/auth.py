"""
Command-line app that lets users register and log in securely.
Uses database-backed authentication from app.services.user_service.
"""


from app.services.user_service import register_user, login_user
from pathlib import Path
import os
import bcrypt

USER_DATA_FILE = Path("DATA") / "users.txt"


def validate_username(username: str):
    """
    Validates username format.
    Returns (is_valid, error_message).
    """
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters."

    if not username.isalnum():
        return False, "Username must contain only letters and numbers."

    return True, ""


def validate_password(password: str):
    """
    Validates password strength.
    Returns (is_valid, error_message).
    """
    if len(password) < 6 or len(password) > 50:
        return False, "Password must be between 6 and 50 characters."

    if not any(c.islower() for c in password):
        return False, "Password must include at least one lowercase letter."

    if not any(c.isupper() for c in password):
        return False, "Password must include at least one uppercase letter."

    if not any(c.isdigit() for c in password):
        return False, "Password must include at least one digit."

    special_chars = "!@#$%^&*()-_=+[]{};:,.<>?/\\|`~\"'"
    if not any(c in special_chars for c in password):
        return False, "Password must include at least one special character."

    return True, ""


def check_password_strength(password: str) -> str:
    """
    Evaluates password strength: "Weak", "Medium", or "Strong".
    """
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1

    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1

    special_chars = "!@#$%^&*()-_=+[]{};:,.<>?/\\|`~\"'"
    if any(c in special_chars for c in password):
        score += 1

    if score <= 3:
        return "Weak"
    elif score <= 5:
        return "Medium"
    else:
        return "Strong"


def display_menu():
    """Displays the main menu options."""
    print("\n" + "=" * 50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("=" * 50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("=" * 50)


def main():
    """Main program loop."""
    print("\nWelcome to the Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1–3): ").strip()

        if choice == "1":
            # Registration flow
            print("\n—— USER REGISTRATION ——")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Optional: show strength
            strength = check_password_strength(password)
            print(f"Password strength: {strength}")

            # Register the user via DB service
            success, message = register_user(username, password)
            print(message)

        elif choice == "2":
            # Login flow
            print("\n—— USER LOGIN ——")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            success, message = login_user(username, password)
            print(message)

            if success:
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard.)")
                input("\nPress Enter to return to main menu...")

        elif choice == "3":
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()