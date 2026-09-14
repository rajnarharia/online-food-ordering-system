import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.db import authenticate_user, create_user, get_foods, get_all_orders

def main():
    print("=" * 50)
    print("      ONLINE FOOD ORDERING SYSTEM (CLI)")
    print("      Note: Please use Streamlit for full experience.")
    print("      Run: streamlit run app.py")
    print("=" * 50)
    
    user = None
    
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. View Menu")
        print("4. Exit")
        choice = input("\nEnter choice: ")
        
        if choice == "1":
            email = input("Email: ")
            pwd = input("Password: ")
            user = authenticate_user(email, pwd)
            if user:
                print(f"Welcome {user['name']}!")
            else:
                print("Invalid credentials.")
        elif choice == "2":
            name = input("Name: ")
            email = input("Email: ")
            pwd = input("Password: ")
            u = create_user(name, email, pwd)
            if u:
                print("Registered! Please login.")
            else:
                print("Email already exists.")
        elif choice == "3":
            foods = get_foods()
            for f in foods:
                print(f"{f['id']}. {f['name']} - Rs.{f['price']}")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()